#include "table.h"
#include <iterator>
#include <algorithm>

#if defined(GENERIC)
ostream & Table::Print(ostream &os) const
{
  // WRITE THIS
  os << "Table()";
  return os;
}
#endif

#if defined(LINKSTATE)
Table::Table() {
    map<pair<unsigned,unsigned>, MapData> tb_map;
}

//Table::Table(int number) {
  //  number = numNode;
//
  //  for(unsigned i = 0; i < numNode ; i++){
//        routingTable.emplace_back(numNode, noEdge);
//    }
//    for(unsigned i = 0; i < numNode ; i++){
//        routingTable[i][i] = 0;
//        if(i == number){
//            costVector.push_back(0);
//        }
//        else{
//        costVector.push_back(noEdge);
//        }
//        nextHopVector.push_back(number);
//    }
//}

// Update Table
unsigned Table::UpdateTable(const RoutingMessage *msg) {
    // Have a link
    cout << msg->GetSrc() << msg->GetDst() << msg->GetLatency() << msg-> GetSeq() << endl;
    if (tb_map.count(make_pair(msg->GetSrc(),msg->GetDst()))) {
        // Duplicate, do nothing
        if (tb_map[make_pair(msg->GetSrc(),msg->GetDst())].seq == msg->GetSeq()) {
            return 0;
        // Update the link
        } else {
            tb_map[make_pair(msg->GetSrc(),msg->GetDst())].latency = msg->GetLatency();
            tb_map[make_pair(msg->GetSrc(),msg->GetDst())].seq = msg->GetSeq();
            return tb_map[make_pair(msg->GetSrc(),msg->GetDst())].seq;
        }
    // Insert a new link
    } else {
        //PrintTable();
        MapData mapData;
        mapData.latency = msg->GetLatency();
        if (msg->GetSeq() == -1) {
            mapData.seq = 0;
        } else {
            mapData.seq = msg->GetSeq();
        }

        //map<int, int> temp;
        //temp[msg->GetSrc()]= msg->GetDst();
        typedef map<pair<int,int>, struct MapData> MapType;
        //studentMap.insert(std::pair<std::pair<int, int>, StudentRecord>(std::make_pair(100, 100), StudentRecord());
        tb_map.insert(MapType::value_type(std::make_pair(msg->GetSrc(),msg->GetDst()), mapData));
        //tb_map.insert(std::pair<std::pair<int, int>, struct MapData>(std::make_pair(msg->GetSrc(), msg->GetDst(), mapData)));
        return mapData.seq;
    }                                        
}

// Print table
void Table::PrintTable() {
    cout << "Print the table" << endl;
    for (map<pair<unsigned, unsigned>, MapData>::const_iterator iter = tb_map.begin(); iter != tb_map.end(); ++iter) {
        cout << "Src: " << (iter)->first.first << " / Dst: " << (iter)->first.second << " / Latency: " << (iter)->second.latency << endl;
    }
}

//map<pair<unsigned, unsigned>, MapData Table::GetTable() const{
//  return tb_map;
//}

map<int, int> Table::MakeRTable(int src) {
    struct RTable rt = Dijkstra(src);
    map<int, int> out;
    for (int i=0; i < rt.nodes.size(); i++) {
        int pre = rt.prevs.at(i);
        int current = pre;
        if (pre != src) {
            while (pre != src) {
                current = pre;
                int pos = find(rt.nodes.begin(), rt.nodes.end(), pre) - rt.nodes.begin();
                pre = rt.prevs.at(pos);
            }
        }
        //cout<< rt.nodes.at(i) << current << endl;
        out.insert(pair<int, int>(rt.nodes.at(i), current));
    }

    return out;
}

struct NeighborTable Table::GetAllNodes(map<pair<unsigned, unsigned>, MapData> tb_m) {
    //get all vertices without duplicates
    struct NeighborTable nt;
    vector<int> nodes;
    map<int, vector<int> > neighbors;
    map<pair<unsigned, unsigned>, MapData >::iterator it;

    // check src
    for (it = tb_m.begin(); it != tb_m.end(); ++it) {
        // src is already counted
        if (find(nodes.begin(), nodes.end(), it->first.first) != nodes.end()) {
            neighbors[it->first.first].push_back(it->first.second);
        // src is not counted yet
        } else {
            nodes.push_back(it->first.first);
            vector<int> k;
            k.push_back(it->first.second);
            neighbors.insert(pair<int, vector<int> >(it->first.first, k));
        }
    }
    vector<int> temp_nodes(nodes);
    // check dst
    for (it = tb_m.begin(); it != tb_m.end(); ++it) {
        // dst is already counted
        if (find(nodes.begin(), nodes.end(), it->first.second) != nodes.end()) {
            ;   //don't do anything in this case
        // src is not counted yet
        } else {
            nodes.push_back(it->first.second);
        }
    }

    nt.nodes = nodes;
    nt.neighbors = neighbors;
    return nt;
}

struct RTable Table::Dijkstra(int src) {
    struct NeighborTable nt = GetAllNodes(tb_map);
    vector<int> vertices = nt.nodes;
    map<int, vector<int> > neighbors = nt.neighbors;
    int V = vertices.size();

    // output
    vector<double> distance;
    vector<int> prev;
    vector<bool> visited;

    // initialization
    for (int i=0; i < V; i++) {
        if (vertices.at(i) == src) {
            distance.push_back(0);
            prev.push_back(src);
        } else {
            distance.push_back(100000000);
            prev.push_back(-1);
        }
        visited.push_back(false);
    }
    for (int i=0; i < V; i++) {
        // Find the vertex with the minimum distance
        int u_index = GetMinVertex(distance, visited);
        visited.at(u_index) = true;

        // Update distance
        int u = vertices.at(u_index);
        if (neighbors.count(u)) {
            vector<int> v = neighbors[u];
            for (vector<int>::iterator it = v.begin(); it !=v.end(); it++) {
                double alt = distance.at(u_index) + tb_map[pair<unsigned, unsigned>(u,*it)].latency;
                int x = find(vertices.begin(), vertices.end(), *it) - vertices.begin();
                if (alt < distance.at(x)) {
                    distance.at(x) = alt;
                    prev.at(x) = u;
                }
            }
        }
    }
    struct RTable rt;
    rt.nodes = vertices;
    rt.prevs = prev;
//  for (vector<int>::const_iterator i = rt.nodes.begin(); i != rt.nodes.end(); ++i)
//      cout << *i << endl;
//  for (vector<int>::const_iterator i = rt.prevs.begin(); i != rt.prevs.end(); ++i)
//      cout << *i << endl;
    return rt;
}

int Table::GetMinVertex(vector<double> distance, vector<bool> visited)
{
    // Initialize min values
    double min = 100000000;
    int min_index;

    for (int i = 0; i < distance.size(); i++) {
        if (visited.at(i) == false && distance.at(i) <= min) {
            min = distance.at(i);
            min_index = i;
        }
    }
    return min_index;
}

ostream & Table::Print(ostream &os) const {
  // WRITE THIS
  os << "Table()";
  return os;
}
#endif

#if defined(DISTANCEVECTOR)

Table::Table() {}

const double Table::noEdge = std::numeric_limits<double>::infinity();

Table::Table(unsigned numNode) {

    number = numNode;

    for(unsigned i = 0; i < numNode ; i++){
        routingTable.emplace_back(numNode, noEdge);
    }
    for(unsigned i = 0; i < numNode ; i++){
        routingTable[i][i] = 0;
        if(i == number){
            costVector.push_back(0);
        }
        else{
        costVector.push_back(noEdge);
        }
        nextHopVector.push_back(number);
    }
}

Table::Table(const Table &rhs) {

    number = rhs.number;
    routingTable = rhs.routingTable;
    costVector = rhs.costVector;
    nextHopVector = rhs.nextHopVector;

}

ostream &Table::Print(ostream &os) const {

    os << "distance vector!" << endl;

    for(unsigned i = 0; i < get_size(); i++){
        for(unsigned j = 0; j < get_size(); j++){

            os << "routingTable[" << i << "][" << j << "] : " << routingTable[i][j] << endl;
        }
    }
    return os;
}

bool Table::change_link(unsigned src, unsigned dest, double cost) {

    unsigned size = get_size();
    unsigned maxSize = max(src, dest);
    maxSize++;

    if(maxSize > size){
        increase(maxSize);
    }
     costVector[dest] = cost;

    return update_Bellman_Ford();
}

bool Table::add_DV(unsigned src, vector<double> message) {

    unsigned size = get_size();
    unsigned dvSize = message.size();
    unsigned maxSize = max(src, dvSize);

    if(maxSize > size){
        increase(maxSize);
    }

    routingTable[src] = message;

    return update_Bellman_Ford();
}

unsigned Table::get_size() const{

    return routingTable.size();
}

void Table::increase(unsigned length) {

    if (length > routingTable.size()){

        unsigned gap = length - routingTable.size();
        unsigned originalSize = routingTable.size();

        for (unsigned i = 0; i < routingTable.size(); i++){
            for(unsigned j = 0; j < gap; j++){
                routingTable[i].push_back(noEdge);
            }
        }

        vector<double> input;
        for (unsigned i = 0; i < length; i++){
            input.push_back(noEdge);
        }

        for(unsigned j = 0; j < gap; j++){
            routingTable.push_back(input);
            costVector.push_back(noEdge);
            nextHopVector.push_back(number);
        }

        for(unsigned j = originalSize; j < originalSize + gap; j++){
            routingTable[j][j] = 0;
        }
    }
}

vector<double> Table::retrieveDV() {

    return routingTable[number];
}

double Table::get_cost(unsigned src, unsigned dest) {

    return routingTable[src][dest];
}

unsigned Table::find_next_node(unsigned destNode){

    return nextHopVector[destNode];
}

bool Table::update_Bellman_Ford() {

    unsigned size = get_size();
    bool result = false;
    
    for (unsigned i = 0; i < size; i++) {

        double oldCost = costVector[i];
        
        if (i != number) {
            
            unsigned nextHop = number;
            priority_queue<double, vector<double>, greater<double> > costQueue;
            double minimum = noEdge;
        
            for (unsigned j = 0; j < size; j++) {
                
                double newCost = costVector[j] + get_cost(j, i);
                costQueue.push(newCost);

                if(newCost <= oldCost){

                    if(newCost == costQueue.top()){
                        minimum = newCost;
                        nextHop = j;
                    }
                }
            }

            if (get_cost(number, i) != minimum) {
                result = true;
            }

            routingTable[number][i] = minimum;
            nextHopVector[i] = nextHop;
        }
    }
    // cerr << "After Bellman_Ford, Table : " << *this<<endl;
    return result;
}


#endif
