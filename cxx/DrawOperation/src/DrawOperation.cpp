#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;

#define WINDOWS_NAME "图片展示"

namespace that {
    int drawRect(Mat&);
}

int main(int argc, char ** argv) {
    std::cout << "绘制矩形"
        << std::endl;
    Mat image = Mat::zeros(800, 800, CV_8UC3);
    return that::drawRect(image);
}

int that::drawRect(Mat& image) {
    Rect rec1 = Rect(100, 300, 600, 200);
    // 虚线
    rectangle(image, rec1, Scalar(0, 0, 255), 1, 1, 0);
    rectangle(image, cv::Point(10, 200), cv::Point(50, 300), Scalar(255, 0, 0), -1, 8, 0);
    imshow(WINDOWS_NAME, image);
    waitKey();
    return 0;
}
