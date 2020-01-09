#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>

using namespace cv;

namespace that {
    void createImg(Mat&);
    void drawColor(int*, int*, int*, Mat&);
}

int main(int arc, char** argv) {
    std::cout << "创建图片与颜色块"
        << std::endl;
    // 创建一个 240宽 320高的 白底图片
    Mat image = Mat(240, 320, CV_8UC3, Scalar(255, 255, 255));
    that::createImg(image);

    Mat hsv, mask, mask_blue, res;
    cv::cvtColor(image, hsv, cv::COLOR_BGR2HSV);

    cv::inRange(hsv, Scalar(100, 43, 46), Scalar(124, 255, 255), mask_blue);
    cv::bitwise_or(mask_blue, mask_blue, mask);
    cv::bitwise_and(image, image, res, mask);

    imshow("image", image);
    imshow("mask", mask);
    imshow("res", res);
    cv::waitKey(0);
    cv::destroyAllWindows();

    return 0;
}

void that::createImg(Mat& image) {
    int rows[] = {100, 140};
    int cols[] = {140, 180};
    int color[] = {0, 0, 255};
    that::drawColor(rows, cols, color, image);
    rows[0] = 60, rows[1] = 100;
    cols[0] = 60, cols[1] = 100;
    color[0] = 0, color[1] = 255, color[2] = 255;
    that::drawColor(rows, cols, color, image);
    cols[0] = 220, cols[1] = 260;
    color[0] = 255, color[1] = 0, color[2] = 0;
    that::drawColor(rows, cols, color, image);
    rows[0] = 140, rows[1] = 180;
    cols[0] = 60, cols[1] = 100;
    that::drawColor(rows, cols, color, image);
    cols[0] = 220, cols[1] = 260;
    color[0] = 0, color[1] = 255, color[2] = 255;
    that::drawColor(rows, cols, color, image);
    rows[0] = 0, rows[1] = 40;
    cols[0] = 0, cols[1] = 40;
    color[0] = 226, color[1] = 43, color[2] = 138;
    that::drawColor(rows, cols, color, image);
    cols[0] = 280, cols[1] = 320;
    color[0] = 209, color[1] = 206, color[2] = 0;
    that::drawColor(rows, cols, color, image);
    rows[0] = 140, rows[1] = 180;
    cols[0] = 140, cols[1] = 180;
    color[0] = 255, color[1] = 0, color[2] = 0;
    that::drawColor(rows, cols, color, image);
}

void that::drawColor(int* rows, int* clos, int* color, Mat& pic) {
    for (auto row = rows[0]; row < rows[1]; row++) {
        for (auto col = clos[0]; col < clos[1]; col++) {
            pic.at<Vec3b>(row, col) = Vec3b(color[0], color[1], color[2]);
        }
    }
}
