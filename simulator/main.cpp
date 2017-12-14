#include <iostream>
#include <drawstuff/drawstuff.h>
#include <thread>
#include <chrono>
#include <string>
#include "kensei.h"
#include "cmdline.h"
#include <grpc++/grpc++.h>

using std::string;
using namespace std::chrono_literals;
using namespace std::this_thread;

int main(int argc, char **argv) {
    cmdline::parser a;

    a.add<string>("address", 'a', "server address", true, "");
    a.add("visible", 'b', "simulator visibility");
    a.parse_check(argc, argv);
    auto address = a.get<string>("address");
    auto visible = a.exist("visible");
    SimulatorServer s;

    grpc::ServerBuilder builder;
    builder.AddListeningPort(address, grpc::InsecureServerCredentials());
    builder.RegisterService(&s);
    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << address << std::endl;
    dInitODE();
    if (visible) {
        enableSlow();
        dsFunctions fn{};
        fn.version = DS_VERSION;
        fn.start = &start;
        fn.step = &simLoop;
        fn.command = &command;
        //fn.path_to_textures = "../../drawstuff/textures";
        fn.path_to_textures = "./textures";

//        auto t = std::thread([] {
////            startSimulation();
////            sleep_for(3s);
////            end();
////            sleep_for(3s);
//
//            startSimulation();
//            sleep_for(3s);
//            simulator::Angle a;
//            a.set_kind(simulator::RIGHT_SHOULDER);
//            a.set_roll(-5);
//            a.set_yaw(-0);
//            a.set_pitch(-0);
//            step(a);
//            a.set_roll(0);
//            a.set_pitch(50);
//            step(a);
//            sleep_for(3s);
//            end();
//        });

        dsSimulationLoop(argc, argv, 800, 600, &fn);
//        t.join();
    } else {
        server->Wait();
    }

    return 0;
}