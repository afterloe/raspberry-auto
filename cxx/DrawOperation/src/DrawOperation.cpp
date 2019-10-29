#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;

#define WINDOWS_NAME "图片展示"

namespace that {
    int drawRect(const Mat&);
}

int main(int argc, char ** argv) {
    std::cout << "绘制矩形"
        << std::endl;
    Mat image = Mat::zeros(800, 800, CV_32F);
    return that::drawRect(image);
}

int that::drawRect(const Mat& image) {
    Rect rec1 = Rect(100, 300, 600, 200);
    rectangle(image, rec1, Scalar(0, 0, 255), -1, 8, 0);
    imshow(WINDOWS_NAME, image);
    waitKey();
    return 0;
}
