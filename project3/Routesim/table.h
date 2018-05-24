#ifndef _table
#define _table


#include <iostream>

using namespace std;

#if defined(GENERIC)
class Table {
  // Students should write this class

 public:
  ostream & Print(ostream &os) const;
};
#endif


#if defined(LINKSTATE)
class Table {
  // Students should write this class
 public:
  ostream & Print(ostream &os) const;
};
#endif

#if defined(DISTANCEVECTOR)

#include <deque>
#include <iostream>
#include <vector>
#include <deque>

class Table {
public:
    Table(unsigned);

    ostream & Print(ostream &os) const;

    static const double noEdge;

    void add_edge(unsigned, unsigned, double);

    unsigned get_size();

    double get_cost(unsigned, unsigned);

    void print_all_cost();

    struct Edge {

        unsigned node1;
        unsigned node2;
        double cost;

        Edge(unsigned n1, unsigned n2, double c) : node1{n1}, node2{n2}, cost{c} {}
    };

    std::vector<Edge> get_all_edges();

    struct Path{

        Path(unsigned);

        std::vector<unsigned> predecessor;
        std::vector<double> distance;
    };

    void relax(Path&, unsigned, unsigned);

    Path Bellman_Ford(unsigned);

    unsigned find_predecessor(unsigned, unsigned);

    unsigned find_next_node(unsigned, unsigned);

    bool check_same(Table&);

    void update_Bellman_Ford();

private:
    std::vector<std::vector<double>> rTable;

};
#endif

inline ostream & operator<<(ostream &os, const Table &t) { return t.Print(os);}


#endif
