//
// Created by afterloe liu on 2019/11/29.
//

#include <opencv2/opencv.hpp>

using namespace cv;

namespace that {
};

const char* keys = {
        "{help h | | print this message}"
        "{@image | | Image to process}"
        "{@lightPattern | | Image light pattern to apply to image input}"
        "{lightMethod | 1 | Method to remove background light, 0 difference, 1 div}"
        "{segMethod | 1 | Method to segment: 1 connected Components, 2 connected components with stats, 3 find Contours}"
};

int main(int argc, char** argv) {
    cv::CommandLineParser parser(argc, argv, keys);
    parser.about("AOIDemo v1.0.0");

    if (parser.has("help")) {
        parser.printMessage();
        return 0;
    }
    std::string img_file = parser.get<std::string>(0);
    std::string light_pattern_file = parser.get<std::string>(1);
    auto method_light = parser.get<int>("lightMethod");
    auto method_seg = parser.get<int>("segMethod");

    if (!parser.check()) {
        parser.printErrors();
        return -1;
    }

    Mat img = imread(img_file, cv::IMREAD_COLOR);
    if (nullptr == img.data) {
        std::cout << "Error loading image " << img_file
        << std::endl;
        return -1;
    }

    imshow("before", img);
    Mat img_noise;
    medianBlur(img, img_noise, 3);
    imshow("noise...", img_noise);
    waitKey(0);
    destroyAllWindows();
}