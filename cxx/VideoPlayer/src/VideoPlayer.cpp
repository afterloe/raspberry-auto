#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>
#include <iostream>

using namespace cv;

namespace vp {
	void guide(char **);
	int process(VideoCapture&);
}

int main(int argc, char** argv) {
	vp::guide(argv);
	VideoCapture cap(0);
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
		for ( ; ; ) {
			capture >> frame;
			if ( frame.empty() ) {
				std::cout << "未连接到设备" << std::endl;
				return -1;
			}
			imshow(windows_name, frame);
			char key = (char) waitKey(1);
			switch (key) {
				case 'q':
				case 'Q':
				case 27:
					return 0;
				default:
					break;
			}
	} catch(std::exception& e) {
		std::cout << "连接异常" << std::endl;
		std::cout << e.what() << std::endl;
	}
	
	return 0;
}
