#ifndef _table
#define _table

#include "messages.h"
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
	//	dst = d;
	//	latency = l;
	//	seq = s;
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

#include <deque>

class Table {
 public:
  ostream & Print(ostream &os) const;
};
#endif

inline ostream & operator<<(ostream &os, const Table &t) { return t.Print(os);}

#endif
