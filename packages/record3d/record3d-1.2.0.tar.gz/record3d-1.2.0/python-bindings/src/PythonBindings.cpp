#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include "record3d/Record3DStream.h"


namespace py = pybind11;


PYBIND11_MODULE( record3d, m )
{
    m.doc() = "Python binding for the C++ library accompanying the Record3D iOS app (https://record3d.app/) which allows to stream RGBD frames.";

    py::class_<Record3D::DeviceInfo>( m, "DeviceInfo" )
            .def_readonly( "product_id", &Record3D::DeviceInfo::productId )
            .def_readonly( "udid", &Record3D::DeviceInfo::udid )
            .def_readonly( "_handle", &Record3D::DeviceInfo::handle )
            ;

    py::class_<Record3D::IntrinsicMatrixCoeffs>( m, "IntrinsicMatrixCoeffs" )
            .def_readonly( "fx", &Record3D::IntrinsicMatrixCoeffs::fx )
            .def_readonly( "fy", &Record3D::IntrinsicMatrixCoeffs::fy )
            .def_readonly( "tx", &Record3D::IntrinsicMatrixCoeffs::tx )
            .def_readonly( "ty", &Record3D::IntrinsicMatrixCoeffs::ty )
            ;

    py::class_<Record3D::Record3DStream>( m, "Record3DStream" )
            .def(py::init<>())
            .def_static( "get_connected_devices", &Record3D::Record3DStream::GetConnectedDevices, "Get IDs of connected devices." )
            .def("disconnect", &Record3D::Record3DStream::Disconnect, "Close connection to currently paired iOS device.")
            .def("connect", &Record3D::Record3DStream::ConnectToDevice, "Connect to iOS device and start receiving RGBD frames.")
            .def("get_depth_frame", &Record3D::Record3DStream::GetCurrentDepthFrame, "Returns the current Depth frame.")
            .def("get_rgb_frame", &Record3D::Record3DStream::GetCurrentRGBFrame, "Return the current RGB frame.")
            .def("get_intrinsic_mat", &Record3D::Record3DStream::GetCurrentIntrinsicMatrix, "Returns the intrinsic matrix of current Depth frame.")
            .def_readwrite("on_new_frame", &Record3D::Record3DStream::onNewFrame, "Method called upon receiving new frame.")
            .def_readwrite("on_stream_stopped", &Record3D::Record3DStream::onStreamStopped, "Method called when stream is interrupted.")
            ;
}