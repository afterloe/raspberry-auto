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
		// 设置视频解吗为 mjpg 解决树莓派 视频播放卡顿的问题
		capture.set(cv::CAP_PROP_FOURCC, cv::VideoWriter::fourcc('M','J','P','G'));
        cv::namedWindow(windows_name, cv::WND_PROP_FULLSCREEN);
        cv::resizeWindow(windows_name, 960, 480);
		for ( ; ; ) {
			capture >> frame;
			if ( frame.empty() ) {
				std::cout << "未连接到设备" << std::endl;
				return -1;
			}
			char key = (char) waitKey(1);
            cv::imshow(windows_name, frame);
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
    cv::destroyAllWindows();
	
	return 0;
}
