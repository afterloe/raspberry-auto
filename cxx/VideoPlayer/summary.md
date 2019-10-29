# C++ 读取并播放视频
> create by [afterloe](605728727@qq.com)  
> MIT License  
> version 1.0  

## 注意事项
### cv下的常量问题
网上很多参数如`CAP_PROP_FOURCC`这类的，在用make编译的时候会出现错误，就算使
用了`using namespace cv`也是一样，所以在这些命名参数上面加上了`cv::`来标识。
而且旧版本的常量在make的过程中会进行提示，可以[参考这里](https://docs.opencv.org/master/d4/d15/group__videoio__flags__base.html#ggaeb8dd9c89c10a5c63c139bf7c4f5704da53e1c28d4c2ca10732af106f3bf00613)。

### 树莓派视频卡顿的问题
同样一段代码，在x64的Ubuntu下没有任何异常，但在树莓派(4G 4b)版本下会
出现卡顿，就算使用官方的[示范代码](./src/officeGruid.cpp)也是一样，google、
baidu了很久也没有找到合适的答案，后来发现python版本的代码没有问题，经过不断
的尝试，发现添加`capture.set(cv::CAP_PROP_FOURCC, cv::VideoWriter::fourcc('M','J','P','G'));`后，卡顿
就消失了，变的十分流畅

## 源码

以下是源代码
```
#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>
#include <iostream>

using namespace cv;

namespace vp {
	void guide(char **);
	int process(VideoCapture&);
}

int main(int argc, char** argv) {
    cv::CommandLineParser parser(argc, argv, "{help h||}{@input||}");
    if (parser.has("help")) {
        vp::guide(argv);
        return 0;
    }
    std::string arg = parser.get<std::string>("@input");
    if (arg.empty()) {
        vp::guide(argv);
        return -1;
    }
	VideoCapture cap(arg);
	if (false == cap.isOpened()) {
		cap.open(0);
	}
	if (false == cap.isOpened()) {
		std::cerr << "打开设备失败" << std::endl;
		return -1;
	}
	return vp::process(cap);
}

void vp::guide(char **argv) {

	std::cout << "调取摄像头播放实时视频" << std::endl
		<< "使用方式: \n" << argv[0] << "<video file>"
		<< std::endl;
}

int vp::process(VideoCapture& capture) {

	auto windows_name = "Live...";
	std::cout << "按下esc 或 q 退出程序" << std::endl;
	Mat frame;

	try {
		auto rate = capture.get(cv::CAP_PROP_FPS);

		// 该项为播放时平时使用
		std::cout << "帧率为: " << rate 
			<< std::endl
			<< "总帧数为: " << capture.get(cv::CAP_PROP_FRAME_COUNT)
			<< std::endl;

		auto position = 0.0;
		capture.set(cv::CAP_PROP_POS_FRAMES, position);
		auto delay = 1000/rate;
		// 设置视频解码为 mjpg 解决树莓派 视频播放卡顿的问题
		capture.set(cv::CAP_PROP_FOURCC, cv::VideoWriter::fourcc('M','J','P','G'));
		for ( ; ; ) {
			capture >> frame;
			if ( frame.empty() ) {
				std::cout << "未连接到设备" << std::endl;
				return -1;
			}
			imshow(windows_name, frame);
			char key = (char) waitKey(delay);
			switch (key) {
				case 'q':
				case 'Q':
				case 27:
					return 0;
				default:
					break;
			}
		}
	} catch(std::exception& e) {
		std::cout << "连接异常" << std::endl;
		std::cout << e.what() << std::endl;
	}
	
	capture.release();
	frame.release();
	
	return 0;
}
```

### 编译
```
cmake_minimum_required(VERSION 2.8)
project( LearnOpencv )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( VideoPlayer.out src/VideoPlayer.cpp )
target_link_libraries( VideoPlayer.out ${OpenCV_LIBS} )
```

### 执行
```
cmake .
make
./VideoPlayer.out
# ./VideoPlayer.out 0 // 播放摄像头采集的视频
# ./VideoPlayer.out path_of_video // 播放本地视频
```
