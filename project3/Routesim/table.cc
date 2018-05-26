#include "table.h"

#if defined(GENERIC)
ostream & Table::Print(ostream &os) const
{
  // WRITE THIS
  os << "Table()";
  return os;
}
#endif

#if defined(LINKSTATE)

#endif

#if defined(DISTANCEVECTOR)

const double Table::noEdge = std::numeric_limits<double>::infinity();

Table::Table(unsigned numNode) {

    for(unsigned i = 0; i < numNode ; i++){
        rTable.emplace_back(numNode, noEdge);
    }
    for(unsigned i = 0; i < numNode ; i++){
        rTable[i][i] = 0;
    }
}

void Table::add_edge(unsigned node1, unsigned node2, double cost) {

    rTable[node1][node2] = cost;
}

unsigned Table::get_size() {

    return rTable.size();
}

double Table::get_cost(unsigned node1, unsigned node2) {

    double result = rTable[node1][node2];
    return result;
}

void Table::print_all_cost() {

    for(unsigned i = 0; i < get_size(); i++){
        for(unsigned j = 0; j < get_size(); j++){

            std::cout << "node " << i << " to " << "node " << j << " is : " << get_cost(i, j) << std::endl;
        }
    }
}

std::vector<Table::Edge> Table::get_all_edges() {

    std::vector<Edge> result;

    for(unsigned i = 0; i < get_size(); i++){
        for(unsigned j = 0; j < i; j++){
            double cost = get_cost(j, i);
            if(cost != Table::noEdge){
                result.emplace_back(j, i, cost);
            }
        }
    }
    return result;
}

Table::Path::Path(unsigned numNode) : predecessor(numNode, numNode), distance(numNode, Table::noEdge) {}

void Table::relax(Table::Path &p1, unsigned node1, unsigned node2){

    double oldCost = p1.distance[node2];
    double newCost = p1.distance[node1] + get_cost(node1, node2);

    if(newCost < oldCost){
        p1.distance[node2] = newCost;
        p1.predecessor[node2] = node1;
    }
}

Table::Path Table::Bellman_Ford(unsigned startNode) {

    unsigned size = get_size();
    Table::Path result(size);

    result.predecessor[startNode] = startNode;
    result.distance[startNode] = 0;

    for(unsigned i = 0; i < size; i++){
        for(auto edge : get_all_edges()){
            relax(result, edge.node1, edge.node2);
        }
    }
    return result;
}

unsigned Table::find_predecessor(unsigned startNode, unsigned destNode) {

    Table::Path pathToLook = Bellman_Ford(startNode);
    unsigned pred = pathToLook.predecessor[destNode];
    return pred;
}

unsigned Table::find_next_node(unsigned startNode, unsigned destNode) {

    Table::Path pathToLook = Bellman_Ford(startNode);

    unsigned interNode = find_predecessor(startNode, destNode);

    if (interNode == startNode){
        return startNode;
    }
    else{
        return find_next_node(interNode, destNode);
    }
}

// if there is a change -> return true
// no change -> return false
bool Table::check_same(Table &t1) {

    unsigned t1Size = t1.get_size();
    unsigned mySize = get_size();

    if (t1Size != mySize){
        return false;
    }
    for(unsigned i = 0; i < mySize; i++){
        for(unsigned j = 0; j < mySize; j++){

            double myCost = get_cost(i, j);
            double t1Cost = t1.get_cost(i, j);

            if(myCost != t1Cost){
                return false;
            }
        }
    }
    return true;
}

void Table::update_Bellman_Ford() {

    unsigned size = get_size();

    for(unsigned i = 0; i < size; i++){
        for(unsigned j = 0; j < size; j++){
            double oldCost = get_cost(i, j);
            for(unsigned k = 0; k < size; k++){
                double newCost = get_cost(i, k) + get_cost(k, j);
                if(newCost < oldCost){
                    rTable[i][j] = newCost;
                }
            }
        }
    }
}

std::vector<double> Table::retrieveVector(unsigned source) {

    return rTable[source];
}


#endif
