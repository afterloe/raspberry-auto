#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;

#define WINDOWS_NAME "图片展示"

namespace that {
    void drawRect(const Mat&);
	void drawLine(const Mat&);
	void drawCircle(const Mat&);
	void writeWord(const Mat&, const std::string&);
}

int main(int argc, char ** argv) {
    std::cout << "绘制矩形"
        << std::endl;
    Mat image = Mat::zeros(800, 800, CV_8UC3);
    that::drawRect(image);
	std::cout << "绘制直线"
		<< std::endl;
	that::drawLine(image);
	that::drawCircle(image);
	std::string word = "石破天惊 - a";
	that::writeWord(image, word);
	imshow(WINDOWS_NAME, image);
	waitKey(0);
}

void that::drawRect(const Mat& image) {
    Rect rec1 = Rect(100, 300, 600, 200);
    // 虚线
    rectangle(image, rec1, Scalar(0, 0, 255), 1, 1, 0);
    rectangle(image, cv::Point(10, 200), cv::Point(50, 300), Scalar(255, 0, 0), -1, 8, 0);
    imshow(WINDOWS_NAME, image);
}

void that::drawLine(const Mat& image) {
	auto x = cv::Point(20, 25),
		 y = cv::Point(200, 400);
	line(image, x, y, Scalar(255,255,9), 1, 8, 0); //虚线
}

void that::drawCircle(const Mat& image) {
	auto point = cv::Point(400, 400);
	auto radius = 45;
	circle(image, point, radius, Scalar(255, 6, 255), 1, 8, 0);
	// 负数 表示实心
	circle(image, cv::Point(750, 50), 50, Scalar(114, 114, 114), -1, 8, 0);
}

void that::writeWord(const Mat& image, const std::string& word) {
	auto point = cv::Point(400, 100);
	auto color = Scalar(110, 110, 100);
	putText(image, word, point, cv::FONT_HERSHEY_SIMPLEX, 1, color, 1, 8, false);
}
