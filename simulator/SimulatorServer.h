//
// Created by kazuki on 17/12/12.
//

#ifndef SIMULATOR_SIMULATORSERVER_H
#define SIMULATOR_SIMULATORSERVER_H

#include "simulator.grpc.pb.h"
#include "simulator.pb.h"

class SimulatorServer final: public simulator::Simulator::Service {
public:
    grpc::Status Start(::grpc::ServerContext *context, const ::simulator::VoidValue *request,
                       ::simulator::VoidValue *response) override;

    grpc::Status
    Send(::grpc::ServerContext *context, const ::simulator::Angle *request, ::simulator::Position *response) override;

    grpc::Status End(::grpc::ServerContext *context, const ::simulator::VoidValue *request,
                     ::simulator::VoidValue *response) override;
};


#endif //SIMULATOR_SIMULATORSERVER_H
