#include "messages.h"


#if defined(GENERIC)
ostream &RoutingMessage::Print(ostream &os) const
{
  os << "RoutingMessage()";
  return os;
}
#endif


#if defined(LINKSTATE)

ostream &RoutingMessage::Print(ostream &os) const
{
  return os;
}

RoutingMessage::RoutingMessage()
{}


RoutingMessage::RoutingMessage(const RoutingMessage &rhs)
{}

#endif


#if defined(DISTANCEVECTOR)

ostream &RoutingMessage::Print(ostream &os) const
{
  return os;
}

RoutingMessage::RoutingMessage(unsigned src, std::vector<double> dv) : srcNode(src), distVector(dv){}

RoutingMessage::RoutingMessage(const RoutingMessage &rhs) : srcNode(rhs.srcNode), distVector(rhs.distVector){}

unsigned RoutingMessage::getSrc() const{

    return srcNode;
}

std::vector<double> RoutingMessage::getDistVector() const{

    return distVector;
}

#endif

