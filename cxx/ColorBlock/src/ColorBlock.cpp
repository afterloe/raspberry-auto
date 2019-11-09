#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>

using namespace cv;

namespace that {

    void createImg(void);
}

int main(int arc, char** argv) {
    std::cout << "创建图片与颜色块"
        << std::endl;
    Mat image = Mat::ones(240, 320, cv::CV_8U) * 3; // make 240 * 320 matrix filled with 3.
    
    imshow("image", image);
    cv::waitKey(0);

    return 0;
}
