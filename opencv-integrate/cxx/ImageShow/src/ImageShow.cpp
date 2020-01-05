#include <iostream>
#include <opencv2/opencv.hpp>

using namespace cv;

#define COMMAND "{help h||print message}{src|<path of image>| string}"
#define WINDOWS_NAME "图片展示"

namespace that {
    void guide(char **);
    int showImage(const std::string&);
}

int main(int argc, char** argv) {
    std::cout << WINDOWS_NAME
        << std::endl;
    cv::CommandLineParser parser(argc, argv, COMMAND);
    if (parser.has("help")) {
        that::guide(argv);
        return 0;
    }
    std::string src = parser.get<std::string>("src");
    if (src.empty()) {
        that::guide(argv);
        return -1;
    }
    return that::showImage(src);
}

int that::showImage(const std::string& src) {
    Mat img;
    std::cout << "msg: " << src << std::endl;
    img = imread(src, -1);
    if (0 == img.data || img.empty()) {
        std::cerr << "读取图片失败" << std::endl;
        return -1;
    }
    imshow(WINDOWS_NAME, img);
    waitKey(0);
    destroyAllWindows();
    return 0;
}

void that::guide(char** argv) {
    std::cout << "图片展示 \r\n"
        << "使用方式: \r\n"
        << argv[0] << " --src path_of_img"
        << std::endl;
}
