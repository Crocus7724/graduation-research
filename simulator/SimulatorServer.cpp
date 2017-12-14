//
// Created by kazuki on 17/12/12.
//

#include "SimulatorServer.h"
#include "kensei.h"
#include <string>

using std::string;

string toString(const simulator::JointKind kind) {
    switch (kind) {
        case simulator::RIGHT_SHOULDER:
            return "right shoulder";
        case simulator::RIGHT_ELBOW:
            return "right elbow";
        case simulator::RIGHT_HIP:
            return "right hip";
        case simulator::RIGHT_KNEE:
            return "right knee";
        case simulator::RIGHT_FOOT:
            return "right foot";
        case simulator::LEFT_SHOULDER:
            return "left shoulder";
        case simulator::LEFT_ELBOW:
            return "left elbow";
        case simulator::LEFT_HIP:
            return "left hip";
        case simulator::LEFT_KNEE:
            return "left knee";
        case simulator::LEFT_FOOT:
            return "left foot";
    }
}

void writeRequest(const simulator::Angle angle) {
    std::cout << "kind: " << toString(angle.kind()) << ", "
              << "roll: " << angle.roll() << ", "
              << "pitch: " << angle.pitch() << ", "
              << "yaw: " << angle.yaw() << std::endl;
}

grpc::Status SimulatorServer::Start(::grpc::ServerContext *context, const ::simulator::VoidValue *request,
                                    ::simulator::VoidValue *response) {
    startSimulation();
    return grpc::Status::OK;
}

grpc::Status SimulatorServer::Send(::grpc::ServerContext *context, const ::simulator::Angle *request,
                                   ::simulator::Position *response) {
//    writeRequest(*request);
    step(*request);
    *response = getPosition(simulator::HEAD);
    return grpc::Status::OK;
}

grpc::Status SimulatorServer::End(::grpc::ServerContext *context, const ::simulator::VoidValue *request,
                                  ::simulator::VoidValue *response) {
    end();
    return grpc::Status::OK;
}