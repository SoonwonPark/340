#include "node.h"
#include "context.h"
#include "error.h"


Node::Node(const unsigned n, SimulationContext *c, double b, double l) : 
    number(n), context(c), bw(b), lat(l) 
{
	  // Create a new table	
	  #if defined(LINKSTATE)
		this-> tb = new Table();
	  #endif
}

Node::Node() 
{ throw GeneralException(); }

Node::Node(const Node &rhs) : 
  number(rhs.number), context(rhs.context), bw(rhs.bw), lat(rhs.lat) {
	#if defined(LINKSTATE)
	  this->tb = rhs.tb;
	#endif
  }

Node & Node::operator=(const Node &rhs) 
{
  return *(new(this)Node(rhs));
}

void Node::SetNumber(const unsigned n) 
{ number=n;}

unsigned Node::GetNumber() const 
{ return number;}

void Node::SetLatency(const double l)
{ lat=l;}

double Node::GetLatency() const 
{ return lat;}

void Node::SetBW(const double b)
{ bw=b;}

double Node::GetBW() const 
{ return bw;}

Node::~Node()
{}

// Implement these functions  to post an event to the event queue in the event simulator
// so that the corresponding node can recieve the ROUTING_MESSAGE_ARRIVAL event at the proper time
void Node::SendToNeighbors(const RoutingMessage *m)
{
//    context->SendToNeighbors(this, m);
	deque<Node*> * neighbors = GetNeighbors();
	deque<Node*>::iterator it;
	cout << neighbors->size() << endl;
	for(it = neighbors->begin(); it != neighbors->end(); it++){
		const RoutingMessage * m_send = new RoutingMessage(*m);
		cout <<"latency: " << m_send->GetLatency() << endl;
		SendToNeighbor(*it,m_send);
	}
}

void Node::SendToNeighbor(const Node *n, const RoutingMessage *m)
{
//context->SendToNeighbor(this, n, m);
	Link * l = new Link();
	l->SetSrc(this->number);
	l->SetDest(n->number);

	const Link * l_copy = new Link(*l);
	Link * l_found = context->FindMatchingLink(l_copy);
	if(l_found != 0) {
		Event * event = new Event(context->GetTime()+l_found->GetLatency(),ROUTING_MESSAGE_ARRIVAL, (void *) n, new RoutingMessage(*m));
		context->PostEvent(event);
	}

	delete l_found;
	delete l;
	cout << "sent to a n" << endl;
}

deque<Node*> *Node::GetNeighbors()
{
  return context->GetNeighbors(this);
}

void Node::SetTimeOut(const double timefromnow)
{
  context->TimeOut(this,timefromnow);
}


bool Node::Matches(const Node &rhs) const
{
  return number==rhs.number;
}


#if defined(GENERIC)
void Node::LinkHasBeenUpdated(const Link *l)
{
  cerr << *this << " got a link update: "<<*l<<endl;
  //Do Something generic:
  SendToNeighbors(new RoutingMessage);
}


void Node::ProcessIncomingRoutingMessage(const RoutingMessage *m)
{
  cerr << *this << " got a routing messagee: "<<*m<<" Ignored "<<endl;
}


void Node::TimeOut()
{
  cerr << *this << " got a timeout: ignored"<<endl;
}

Node *Node::GetNextHop(const Node *destination) const
{
  return 0;
}

Table *Node::GetRoutingTable() const
{
  return new Table;
}


ostream & Node::Print(ostream &os) const
{
  os << "Node(number="<<number<<", lat="<<lat<<", bw="<<bw<<")";
  return os;
}

#endif

#if defined(LINKSTATE)
//Node::Node(const Node &rhs) : number(rhs.number), context(rhs.context), bw(rhs.bw), lat(rhs.lat) {}

void Node::LinkHasBeenUpdated(const Link *l)
{
  cerr << *this<<": Link Update: "<<*l<<endl;
  RoutingMessage * m = new RoutingMessage(l->GetSrc(), l->GetDest(), l->GetLatency(), -1);
  //update table
  unsigned seq;
  seq = tb->UpdateTable(m);
  //send new info to neighbors
  m->SetSeq(seq);
  SendToNeighbors(m);
  cout << "1" << endl;
}


void Node::ProcessIncomingRoutingMessage(const RoutingMessage *m)
{
cout << "2" << endl; 
  	cerr << *this << " Routing Message: "<<*m;
  if (tb->UpdateTable(m)!=0) {
      SendToNeighbors(m);
  }
}

void Node::TimeOut()
{
  cerr << *this << " got a timeout: ignored"<<endl;
}

Node *Node::GetNextHop(const Node *destination)
{
	cerr << *this << " Getting Next hop: "<<*destination << endl;
	if(number == destination->number)
		return this;
	map<int, int> rtable = tb->MakeRTable(number);
	int nextHop = rtable[destination->number];
	// create the return
	deque<Node*> *n = this->GetNeighbors();
	for (deque<Node*>::const_iterator i = n->begin(); i != n->end(); ++i) {
		if ((Node(nextHop, 0, 0, 0).Matches(**i))) {
			return new Node(**i); // change to new node **i
		}
	}
   return 0;	
}

Table *Node::GetRoutingTable() const
{
  return tb;
}

ostream & Node::Print(ostream &os) const
{
  os << "Node(number="<<number<<", lat="<<lat<<", bw="<<bw<<")";
  return os;
}
#endif


#if defined(DISTANCEVECTOR)

void Node::LinkHasBeenUpdated(const Link *l)
{
  // update our table
  // send out routing mesages
  cerr << *this<<": Link Update: "<<*l<<endl;
}


void Node::ProcessIncomingRoutingMessage(const RoutingMessage *m)
{

}

void Node::TimeOut()
{
  cerr << *this << " got a timeout: ignored"<<endl;
}


Node *Node::GetNextHop(const Node *destination) const
{
}

Table *Node::GetRoutingTable() const
{
}


ostream & Node::Print(ostream &os) const
{
  os << "Node(number="<<number<<", lat="<<lat<<", bw="<<bw;
  return os;
}
#endif
