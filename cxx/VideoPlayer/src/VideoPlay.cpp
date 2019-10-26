#include <stdio.h>
#include <opencv2/opencv.hpp>

using namespace cv;

#define DEVICE_ID 0
#define API_ID cv::CAP_ANY

int main(int argc, char** argv) {


	Mat frame;
	VideoCapture cap;

	cap.open(DEVICE_ID + API_ID);
	if(false == cap.isOpened()) {
		std::cerr << "can't open vidoe." << std::endl;
		return -1;
	}

	std::cout << "Strt grabbing." << std::endl;
	for ( ; ; ) {
		cap.read(frame);
		if (frame.empty()) {
			std::cerr << "ERROR! blank frame grabbed" << std::endl;
			break;
		}
		imshow("Live", frame);
		if (27 == waitKey(10)) {
			std::cout << "pressing esc ..." << std::endl;
			break;
		}
	}

	return 0;
}
