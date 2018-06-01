#include "messages.h"


#if defined(GENERIC)
ostream &RoutingMessage::Print(ostream &os) const
{
  os << "RoutingMessage()";
  return os;
}
#endif


#if defined(LINKSTATE)

ostream &RoutingMessage::Print(ostream &os) const {
  return os;
}

RoutingMessage::RoutingMessage()
{}

RoutingMessage::RoutingMessage(const RoutingMessage &rhs) :
	source(rhs.source), destination(rhs.destination), latency(rhs.latency), sequence(rhs.sequence) {}

RoutingMessage::RoutingMessage(unsigned src, unsigned dst, double lat, unsigned seq) :
	source(src), destination(dst), latency(lat), sequence(seq) {}

unsigned RoutingMessage::GetSrc() const {
   	return source;
}

unsigned RoutingMessage::GetDst() const {
	return destination;
}

double RoutingMessage::GetLatency() const {
	return latency;
}  

unsigned RoutingMessage::GetSeq() const {
	return sequence;
}

void RoutingMessage::SetSeq(const unsigned seq) {
	sequence = seq;
}

#endif


#if defined(DISTANCEVECTOR)

ostream &RoutingMessage::Print(ostream &os) const
{
  return os;
}

RoutingMessage::RoutingMessage()
{}


RoutingMessage::RoutingMessage(const RoutingMessage &rhs)
{}

#endif

