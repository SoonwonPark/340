#ifndef _table
#define _table

#include <iostream>
#include <map>
#include <vector>

using namespace std;

#if defined(GENERIC)
class Table {
  // Students should write this class

 public:
  ostream & Print(ostream &os) const;
};
#endif


#if defined(LINKSTATE)
#include "messages.h"
struct NeighborTable {
  public:
    vector<int> nodes;
    map<int, vector<int> > neighbors;
};

struct RTable {
  public:
    vector<int> nodes;
    vector<int> prevs;
};

struct MapData {
  public:
    double latency;
    unsigned seq;
    //MapData(unsigned d, double l, unsigned s) {
    //  dst = d;
    //  latency = l;
    //  seq = s;
    //}
};

class Table {
  // Students should write this class
 public:
    map<pair<unsigned,unsigned>, MapData> tb_map;

    Table();

    Table(int number);

    unsigned UpdateTable(const RoutingMessage *msg);

    void PrintTable();

    map<int, int> MakeRTable(int src);

    struct NeighborTable GetAllNodes(map<pair<unsigned, unsigned>, MapData> tb_m);

    struct RTable Dijkstra(int src);

    int GetMinVertex(vector<double> distance, vector<bool> visited);

    ostream & Print(ostream &os) const;
};
#endif

#if defined(DISTANCEVECTOR)

#include <queue>
#include <deque>
#include <limits>
#include <cmath>
#include <algorithm>

class Table {

public:

    Table();

    Table(unsigned);
    
    Table(const Table&);
    
    static const double noEdge;
    
    ostream & Print(ostream &os) const;
    
    bool change_link(unsigned, unsigned, double);
    
    bool add_DV(unsigned, vector<double>);
    
    unsigned get_size() const;
    
    double get_cost(unsigned, unsigned);
    
    void increase(unsigned);
    
    vector<double> retrieveDV();
    
    unsigned find_next_node(unsigned);
    
    bool update_Bellman_Ford();


private:

    unsigned number;

    std::vector<std::vector<double> > routingTable;

    vector<double> costVector;

    vector<unsigned> nextHopVector;

};
#endif

inline ostream & operator<<(ostream &os, const Table &t) { return t.Print(os);}

#endif










