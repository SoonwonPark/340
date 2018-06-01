touch .dependencies
make depend
make TYPE=LINKSTATE clean depend all
./routesim demo.topo demo.event
