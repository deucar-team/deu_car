// Generated by gencpp from file deu_ros/WordCount.msg
// DO NOT EDIT!


#ifndef DEU_ROS_MESSAGE_WORDCOUNT_H
#define DEU_ROS_MESSAGE_WORDCOUNT_H

#include <ros/service_traits.h>


#include <deu_ros/WordCountRequest.h>
#include <deu_ros/WordCountResponse.h>


namespace deu_ros
{

struct WordCount
{

typedef WordCountRequest Request;
typedef WordCountResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct WordCount
} // namespace deu_ros


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::deu_ros::WordCount > {
  static const char* value()
  {
    return "58903d21a3264f3408d79ba79e9f7c7e";
  }

  static const char* value(const ::deu_ros::WordCount&) { return value(); }
};

template<>
struct DataType< ::deu_ros::WordCount > {
  static const char* value()
  {
    return "deu_ros/WordCount";
  }

  static const char* value(const ::deu_ros::WordCount&) { return value(); }
};


// service_traits::MD5Sum< ::deu_ros::WordCountRequest> should match
// service_traits::MD5Sum< ::deu_ros::WordCount >
template<>
struct MD5Sum< ::deu_ros::WordCountRequest>
{
  static const char* value()
  {
    return MD5Sum< ::deu_ros::WordCount >::value();
  }
  static const char* value(const ::deu_ros::WordCountRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::deu_ros::WordCountRequest> should match
// service_traits::DataType< ::deu_ros::WordCount >
template<>
struct DataType< ::deu_ros::WordCountRequest>
{
  static const char* value()
  {
    return DataType< ::deu_ros::WordCount >::value();
  }
  static const char* value(const ::deu_ros::WordCountRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::deu_ros::WordCountResponse> should match
// service_traits::MD5Sum< ::deu_ros::WordCount >
template<>
struct MD5Sum< ::deu_ros::WordCountResponse>
{
  static const char* value()
  {
    return MD5Sum< ::deu_ros::WordCount >::value();
  }
  static const char* value(const ::deu_ros::WordCountResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::deu_ros::WordCountResponse> should match
// service_traits::DataType< ::deu_ros::WordCount >
template<>
struct DataType< ::deu_ros::WordCountResponse>
{
  static const char* value()
  {
    return DataType< ::deu_ros::WordCount >::value();
  }
  static const char* value(const ::deu_ros::WordCountResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // DEU_ROS_MESSAGE_WORDCOUNT_H
