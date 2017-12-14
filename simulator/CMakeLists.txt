cmake_minimum_required(VERSION 3.9)
project(simulator)

set(COMPILE_FILES main.cpp kensei.cpp kensei.h SimulatorServer.cpp SimulatorServer.h)

set(CMAKE_CXX_STANDARD 14)

link_libraries(ode drawstuff GL GLU glut X11 pthread)


# grpc
find_package(Protobuf REQUIRED)
set(PROTO_PATH "${CMAKE_SOURCE_DIR}/../proto")
set(SIMULATOR_PROTO "${PROTO_PATH}/simulator.proto")
set(GENERATED_PROTOBUF_PATH "${CMAKE_BINARY_DIR}/generated")
file(MAKE_DIRECTORY ${GENERATED_PROTOBUF_PATH})

set(SIMULATOR_PB_CPP_FILE "${GENERATED_PROTOBUF_PATH}/simulator.pb.cc")
set(SIMULATOR_PB_H_FILE "${GENERATED_PROTOBUF_PATH}/simulator.pb.h")
set(SIMULATOR_GRPC_PB_CPP_FILE "${GENERATED_PROTOBUF_PATH}/simulator.grpc.pb.cc")
set(SIMULATOR_GRPC_PB_H_FILE "${GENERATED_PROTOBUF_PATH}/simulator.grpc.pb.h")

add_custom_command(
        OUTPUT "${SIMULATOR_PB_H_FILE}"
        "${SIMULATOR_PB_CPP_FILE}"
        "${SIMULATOR_GRPC_PB_H_FILE}"
        "${SIMULATOR_GRPC_PB_CPP_FILE}"
        COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
        ARGS "--proto_path=${PROTO_PATH}"
        "--cpp_out=${GENERATED_PROTOBUF_PATH}"
        "${SIMULATOR_PROTO}"
        COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
        ARGS "--proto_path=${PROTO_PATH}"
        "--grpc_out=${GENERATED_PROTOBUF_PATH}"
        "--plugin=protoc-gen-grpc=/usr/local/bin/grpc_cpp_plugin"
        "${SIMULATOR_PROTO}"
)

set(GENERATED_PROTOBUF_FILES "${SIMULATOR_PB_H_FILE}" "${SIMULATOR_PB_CPP_FILE}" "${SIMULATOR_GRPC_PB_H_FILE}" "${SIMULATOR_GRPC_PB_CPP_FILE}" cmdline.h)
include_directories(${GENERATED_PROTOBUF_PATH})
link_libraries(grpc++_unsecure grpc gpr ${PROTOBUF_LIBRARY})

add_executable(simulator ${COMPILE_FILES} ${GENERATED_PROTOBUF_FILES})
