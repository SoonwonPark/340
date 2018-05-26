#ifndef _messages
#define _messages

#include <iostream>

#include "node.h"
#include "link.h"

#if defined(GENERIC)
class RoutingMessage {
 public:
  ostream & Print(ostream &os) const;
};
#endif

#if defined(LINKSTATE)
class RoutingMessage {

  RoutingMessage();
  RoutingMessage(const RoutingMessage &rhs);
  RoutingMessage &operator=(const RoutingMessage &rhs);

  ostream & Print(ostream &os) const;
};
#endif

#if defined(DISTANCEVECTOR)
class RoutingMessage {

public:
    RoutingMessage();
    RoutingMessage(unsigned src, std::vector<double> dv);
    RoutingMessage(const RoutingMessage &rhs);
    RoutingMessage &operator=(const RoutingMessage &rhs);
    unsigned getSrc() const;
    std::vector<double> getDistVector() const;
    ostream & Print(ostream &os) const;

private:
    unsigned srcNode;
    std::vector<double> distVector;
};
#endif


inline ostream & operator<<(ostream &os, const RoutingMessage &m) { return m.Print(os);}

#endif
