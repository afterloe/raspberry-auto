#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>

using namespace cv;

namespace that {

    void createImg(void);
}

int main(int arc, char** argv) {
    std::cout << "创建图片与颜色块"
        << std::endl;
    // 创建一个 240宽 320高的 白底图片
    Mat image = Mat::ones(240, 320, CV_8UC1) * 255; 



    imshow("image", image);
    cv::waitKey(0);

    return 0;
}
