/**
 *  create by afterloe
 *
 *  version is 1.0 MIT License
 */
#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>

namespace that {
    void guide(char **);
}

int main(int argc, char** argv) {
    std::cout << "人脸识别模块"
        << std::endl;
    cv::CommandLineParser parser(argc, argv, "{help h ||}{@src ||}{@video ||}");
    if (parser.has("help")) {
        that::guide(argv);
        return 0;
    }
    std::string flag = parset.get<std::string>("video");
    if ("" != flag) {
        // open video to catch face
        
    } else {
        // readImage to find face
    }

    return 0;
}

void that::guide(char **argv) {
    std::cout << "src -> to you pic of path"
        << std::endl
        << "video -> open your video to catch face, any value."
        << std::endl;
}
