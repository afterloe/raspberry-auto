#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;

int main(int argc, char** argv) {

	VideoCapture cap(0);
	if (false == cap.isOpened()) {
		std::cout << "Can't open this video." << std::endl;
		return -1;
	}

	for ( ; ; ) {
		Mat frame;
		cap >> frame;
		if ( frame.empty() ) {
			break;
		}
		imshow("raspberry video", frame);
		if ( 27 == waitKey(10)) {
			std::cout << "pressing esc ..." << std::endl;
			break;
		}

	}

	// cpa.close(); // 当程序exit的时候， 自动调用
	return 0;
}
