/**
 * The AbstractInstanceParser is in charge of populating the instance specific data structures (x and y
 * coordinates, customer demands, cost matrix, neighbor matrix, etc...) starting from an input instance file.
 *
 * The specific parser implementation is delegated to AbstractInstanceParser sub-classes that implement the
 * parse_impl method.
 *
 */

#ifndef COBRA_ABSTRACTINSTANCEPARSER_HPP
#define COBRA_ABSTRACTINSTANCEPARSER_HPP

#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include "mm.hpp"
#include <time.h>
#include "Flat2DVector.hpp"
#include <curl/curl.h>
#include <jsoncpp/json/value.h>
#include <jsoncpp/json/json.h>

namespace cobra
{

    template <bool round_costs = true>
    class AbstractInstanceParser
    {

    public:
        explicit AbstractInstanceParser(const std::string &path_) : path(path_) {}

        static size_t WriteCallback(char *contents, size_t size, size_t nmemb, char *buffer_in)
        {
            ((std::string *)buffer_in)->append((char *)contents, size * nmemb);
            return size * nmemb;
        }

        bool parse()
        {

            CURL *curl = curl_easy_init();
            Json::Value json;
            Json::CharReaderBuilder jsonBuilder;
            Json::Reader reader;
            Json::CharReader *JsonReader(jsonBuilder.newCharReader());
            double distance;
            // std::string tmp = "http://ec2-34-222-175-250.us-west-2.compute.amazonaws.com/table/v1/driving/";
            std::string tmp = "http://localhost:5000/table/v1/driving/";
            std::string errors;
            std::string readBuffer;

            auto ok = parse_impl();
            if (!ok)
            {
                return ok;
            }

            auto matrix_size = static_cast<int>(demands.size());

            costs_matrix.resize(matrix_size, matrix_size);

            std::cout << "Calculando distâncias" << std::endl;

            //CONFIGURA URL DA REQUISICAO
            for (auto i = 0; i < matrix_size - 1; i++)
            {
                tmp = tmp + std::to_string(x_coordinates[i]) + "," + std::to_string(y_coordinates[i]) + ";";
            }
            tmp.pop_back();
            tmp = tmp + "?annotations=distance";
            //std::cout << tmp << std::endl;
            tempoAPI = clock();
            // CHAMADA DA API
            if (curl)
            {
                curl_easy_setopt(curl, CURLOPT_URL, tmp.c_str());
                curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
                curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

                curl_easy_perform(curl);
                //reader.parse(readBuffer, json);
                const auto is_parsed = JsonReader->parse(readBuffer.c_str(),
                                                         readBuffer.c_str() + readBuffer.length(),
                                                         &json,
                                                         &errors);

                if (!is_parsed)
                {
                    std::cerr << "ERROR: Could not parse! " << errors << '\n';
                    return -1;
                }
            }
            tempoAPI = clock() - tempoAPI;
            //GUARDA RESPOSTA NA MATRIX
            for (auto i = 0; i < matrix_size - 1; i++)
            {

                costs_matrix.at(i, i, 0.0f);

                for (auto j = i + 1; j < matrix_size; j++)
                {
                    costs_matrix.at(i, j, json["distances"][i][j].asFloat());
                    if constexpr (round_costs)
                    {
                        costs_matrix.at(i, j, std::round(costs_matrix.at(i, j)));
                    }

                    costs_matrix.at(j, i, costs_matrix.at(i, j));
                }
            }

            std::cout << "Tempo das chamadas API = " + std::to_string(((float)tempoAPI) / CLOCKS_PER_SEC) << std::endl;

            curl_easy_cleanup(curl);
            neighbors.resize(matrix_size);

            auto all_vertices = std::vector<int>(matrix_size);

            for (auto i = 0; i < matrix_size; i++)
            {
                all_vertices[i] = i;
            }
            tempoSort = clock();
            for (auto i = 0; i < matrix_size; i++)
            {

                std::sort(all_vertices.begin(),
                          all_vertices.end(),
                          [this, i](auto j, auto k)
                          { return costs_matrix.at(i, j) < costs_matrix.at(i, k); });

                neighbors[i] = all_vertices;

                // make sure the first vertex is i
                if (neighbors[i][0] != i)
                {
                    auto n = 1;
                    while (n < matrix_size)
                    {
                        if (neighbors[i][n] == i)
                        {
                            break;
                        }
                        n++;
                    }
                    std::swap(neighbors[i][0], neighbors[i][n]);
                }

                assert(neighbors[i][0] == i);
            }
            tempoSort = clock() - tempoSort;
            std::cout << "Tempo ordenação = " + std::to_string(((float)tempoSort) / CLOCKS_PER_SEC) << std::endl;

            return ok;
        }

        virtual bool parse_impl() = 0;

        int get_vehicle_capacity() { return vehicle_capacity; }

        std::vector<float> get_x_coordinates() { return x_coordinates; }

        std::vector<float> get_y_coordinates() { return y_coordinates; }

        std::vector<int> get_demands() { return demands; }

        Flat2DVector<float> get_costs_matrix() { return costs_matrix; }

        std::vector<std::vector<int>> get_neighbors() { return neighbors; }

        clock_t getTempoAPI() { return tempoAPI; }

        clock_t getTempoSort() { return tempoSort; }

    protected:
        clock_t tempoAPI;
        clock_t tempoSort;
        const std::string &path;
        int vehicle_capacity{};
        std::vector<float> x_coordinates;
        std::vector<float> y_coordinates;
        std::vector<int> demands;

    private:
        Flat2DVector<float> costs_matrix;
        std::vector<std::vector<int>> neighbors;
    };

    inline std::vector<std::string> split_line(const std::string &line, char separator)
    {

        auto tokens = std::vector<std::string>();

        auto stream = std::istringstream(line);
        auto token = std::string();

        while (std::getline(stream, token, separator))
        {
            tokens.emplace_back(token);
        }

        return tokens;
    }

    template <bool round_costs>
    class XInstanceParser : public AbstractInstanceParser<round_costs>
    {

    public:
        explicit XInstanceParser(const std::string &path_) : AbstractInstanceParser<round_costs>(path_) {}

        bool parse_impl()
        {

            try
            {

                std::ifstream stream(this->path);

                if (!stream)
                {
                    throw std::exception();
                }

                std::string line;
                std::string::size_type sz = 0;

                // skip 3 lines
                std::getline(stream, line);
                std::getline(stream, line);
                std::getline(stream, line);

                // dimension
                std::getline(stream, line);
                std::stringstream ss(line);
                std::getline(ss, line, ':');
                std::getline(ss, line, '\n');
                auto matrix_size = stoi(line, &sz);
                line.erase(0, sz);

                // skip 1 line
                std::getline(stream, line);

                // capacity
                std::getline(stream, line);
                std::stringstream ss2(line);
                std::getline(ss2, line, ':');
                std::getline(ss2, line, '\n');
                this->vehicle_capacity = stoi(line, &sz);
                line.erase(0, sz);

                // skip 1 line
                std::getline(stream, line);

                this->x_coordinates.resize(matrix_size);
                this->y_coordinates.resize(matrix_size);
                this->demands.resize(matrix_size);

                // coord section
                for (auto n = 0; n < matrix_size; n++)
                {

                    std::getline(stream, line);

                    stoi(line, &sz); // index
                    line.erase(0, sz);

                    this->x_coordinates[n] = stof(line, &sz);
                    line.erase(0, sz);

                    this->y_coordinates[n] = stof(line, &sz);
                    line.erase(0, sz);
                }

                // demand section
                std::getline(stream, line);
                for (auto n = 0; n < matrix_size; n++)
                {

                    std::getline(stream, line);

                    stoi(line, &sz); // index
                    line.erase(0, sz);

                    this->demands[n] = stoi(line, &sz);
                    line.erase(0, sz);
                }
            }
            catch (std::exception &e)
            {
                return false;
            }
            return true;
        }
    };

    template <bool round_costs>
    class KytojokiInstanceParser : public AbstractInstanceParser<round_costs>
    {

    public:
        explicit KytojokiInstanceParser(const std::string &path_) : AbstractInstanceParser<round_costs>(path_) {}

        bool parse_impl()
        {

            try
            {

                std::ifstream stream(this->path);

                if (!stream)
                {
                    throw std::exception();
                }

                std::string line;

                // skip 1 line
                std::getline(stream, line);

                std::getline(stream, line);
                auto tokens = split_line(line, '\t');
                auto matrix_size = std::stoi(tokens[1]);
                this->vehicle_capacity = std::stoi(tokens[2]);

                this->x_coordinates.resize(matrix_size);
                this->y_coordinates.resize(matrix_size);
                this->demands.resize(matrix_size);

                // depot
                this->x_coordinates[0] = std::stof(tokens[3]);
                this->y_coordinates[0] = std::stof(tokens[4]);
                this->demands[0] = 0;

                // customers
                for (auto n = 1; n < matrix_size; n++)
                {

                    std::getline(stream, line);
                    tokens = split_line(line, '\t');

                    this->x_coordinates[n] = std::stof(tokens[14]);
                    this->y_coordinates[n] = std::stof(tokens[15]);
                    this->demands[n] = std::stoi(tokens[7]);
                }
            }
            catch (std::exception &e)
            {
                return false;
            }
            return true;
        }
    };

    template <bool round_costs>
    class ZKInstanceParser : public AbstractInstanceParser<round_costs>
    {

    public:
        explicit ZKInstanceParser(const std::string &path_) : AbstractInstanceParser<round_costs>(path_) {}

        bool parse_impl()
        {

            try
            {

                std::ifstream stream(this->path);

                if (!stream)
                {
                    throw std::exception();
                }

                std::string line;

                std::getline(stream, line);
                auto tokens = split_line(line, '\t');
                auto matrix_size = std::stoi(tokens[0]) + 1; // number of customers + 1
                this->vehicle_capacity = std::stoi(tokens[1]);

                this->x_coordinates.resize(matrix_size);
                this->y_coordinates.resize(matrix_size);
                this->demands.resize(matrix_size);

                // customers
                for (auto n = 0; n < matrix_size; n++)
                {

                    std::getline(stream, line);

                    tokens = split_line(line, '\t');

                    this->x_coordinates[n] = std::stof(tokens[1]);
                    this->y_coordinates[n] = std::stof(tokens[2]);
                    this->demands[n] = std::stoi(tokens[3]);
                }
            }
            catch (std::exception &e)
            {
                return false;
            }
            return true;
        }
    };

}

#endif //COBRA_ABSTRACTINSTANCEPARSER_HPP
