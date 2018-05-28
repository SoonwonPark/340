touch .dependencies
make depend
make TYPE=LINKSTATE
./routesim demo.topo demo.event
