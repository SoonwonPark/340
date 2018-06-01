#ifndef _messages
#define _messages

#include "node.h"
#include "link.h"
#include <iostream>
#include <vector>

#if defined(GENERIC)
class RoutingMessage {
 public:
  ostream & Print(ostream &os) const;
};
#endif

#if defined(LINKSTATE)
class RoutingMessage {
  public:
  unsigned source;
  unsigned destination;
  double latency;
  unsigned sequence;

  RoutingMessage();
    RoutingMessage(const RoutingMessage &rhs);
    RoutingMessage &operator=(const RoutingMessage &rhs);
    RoutingMessage(unsigned src, unsigned dst, double lat, unsigned seq);

  unsigned GetSrc() const;
  unsigned GetDst() const;
  double GetLatency() const;
  unsigned GetSeq() const;
  void SetSeq(unsigned seq);
    ostream & Print(ostream &os) const;
};
#endif

#if defined(DISTANCEVECTOR)
class RoutingMessage {

public:
    RoutingMessage();
    RoutingMessage(const RoutingMessage &rhs);
    RoutingMessage(unsigned src, vector<double> dv);
    RoutingMessage &operator=(const RoutingMessage &rhs);
    unsigned get_source() const;
    vector<double> get_dv() const;
    ostream & Print(ostream &os) const;

private:
    unsigned node;
    vector<double> myDV;
};
#endif


inline ostream & operator<<(ostream &os, const RoutingMessage &m) { return m.Print(os);}

#endif
