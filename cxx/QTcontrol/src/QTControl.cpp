//
// Created by afterloe liu on 2019/11/29.
//

#include <string>
#include <cmath>
using namespace std;

#include <opencv2/core/utility.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
using namespace cv;

cv::Mat image;

namespace that {
    void showHistoCallback(int, void*);
    void equalizeCallback(int, void*);
    void lomoCallback(int, void*);
    void cartoonCallback(int, void*);
};

const char* key = {
        "{help h usage ? | | print this message}"
        "{@image | | Image to process}"
};

int main(int argc, char** argv) {
    cv::CommandLineParser parser(argc, argv, key);
    parser.about("Chapter 4. PhotoTool v1.0.0");

    if (parser.has("help")) {
        parser.printMessage();
        return 0;
    }

    std::string imgFile = parser.get<std::string>("@image");

    if(!parser.check()) {
        parser.printErrors();
        return -1;
    }

    image = cv::imread(imgFile, cv::IMREAD_COLOR);
    cv::namedWindow("input pic");
    createButton("Show histogram", that::showHistoCallback, NULL, QT_PUSH_BUTTON, 0);
    createButton("Equalize histogram", that::equalizeCallback, NULL, QT_PUSH_BUTTON, 0);
    createButton("Lomography effect", that::lomoCallback, NULL, QT_PUSH_BUTTON, 0);
    createButton("Cartonize effect", that::cartoonCallback, NULL, QT_PUSH_BUTTON, 0);

    cv::imshow("input pic", image);

    cv::waitKey(0);
    return 0;
}

void that::showHistoCallback(int, void*) {
    std::vector<cv::Mat> bgr;
    split(image, bgr);
    int numbins = 256;
    float range[] = {0, 256};
    const float* histRange = {range};

    cv::Mat b_hist, g_hist, r_hist;
    cv::calcHist(&bgr[0], 1, 0, cv::Mat(), b_hist, 1, &numbins, &histRange);
    cv::calcHist(&bgr[1], 1, 0, cv::Mat(), g_hist, 1, &numbins, &histRange);
    cv::calcHist(&bgr[2], 1, 0, cv::Mat(), r_hist, 1, &numbins, &histRange);

    int width = 512;
    int height = 300;
    cv::Mat histImage(height, width, CV_8UC3, cv::Scalar(20, 20, 20));

    cv::normalize(b_hist, b_hist, 0, height, cv::NORM_MINMAX);
    cv::normalize(g_hist, g_hist, 0, height, cv::NORM_MINMAX);
    cv::normalize(r_hist, r_hist, 0, height, cv::NORM_MINMAX);

    int binStep = cvRound((float)width / (float)numbins);
    for (auto i = 1; i < numbins; i++) {
        cv::line(histImage,
                cv::Point(binStep*(i - 1), height - cvRound(b_hist.at<float>(i -1))),
                cv::Point(binStep*(i), height - cvRound(b_hist.at<float>(i))),
                Scalar(255, 0, 0)
                );
        cv::line(histImage,
                 cv::Point(binStep*(i - 1), height - cvRound(b_hist.at<float>(i -1))),
                 cv::Point(binStep*(i), height - cvRound(b_hist.at<float>(i))),
                 Scalar(0, 255, 0)
        );
        cv::line(histImage,
                 cv::Point(binStep*(i - 1), height - cvRound(b_hist.at<float>(i -1))),
                 cv::Point(binStep*(i), height - cvRound(b_hist.at<float>(i))),
                 Scalar(0, 0, 255)
        );
    }

    cv::imshow("Histogram", histImage);
}

void that::equalizeCallback(int, void*) {
    cv::Mat result;
    cv::Mat ycrcb;

    cvtColor(image, ycrcb, cv::COLOR_BGR2YCrCb);
    std::vector<cv::Mat> channels;
    split(ycrcb, channels);
    cv::equalizeHist(channels[0], channels[0]);
    cv::merge(channels, ycrcb);
    cv::cvtColor(ycrcb, result, cv::COLOR_BGR2YCrCb);

    cv::imshow("Equalized", result);
}

void that::lomoCallback(int, void *) {
    cv::Mat result;

    const double E = std::exp(1.0);
    cv::Mat lut(1, 256, CV_8UC1);
    for (auto i = 0; i < 256; i++) {
        float x = (float) i / 256.0;
        lut.at<uchar>(i) = cvRound(256 * ( 1 / (1 + pow(E, -((x - 0.5) / 0.1 )))));
    }

    std::vector<cv::Mat> bgr;
    split(image, bgr);
    LUT(bgr[2], lut, bgr[2]);
    cv::merge(bgr, result);
    cv::Mat halo(image.rows, image.cols, CV_32FC3, Scalar(0.3, 0.3, 0.3));
    cv::circle(halo, cv::Point(image.cols / 2, image.rows / 2), image.cols / 3, cv::Scalar(1, 1, 1), -1);
    cv::blur(halo, halo, Size(image.cols / 3, image.cols / 3));

    cv::Mat resultf;
    result.convertTo(resultf, CV_32FC3);
    multiply(resultf, halo, resultf);

    resultf.convertTo(result, CV_8UC3);

    cv::imshow("Lomograpy", result);

    halo.release();
    resultf.release();
    lut.release();
    bgr[0].release();
    bgr[1].release();
    bgr[2].release();
}

void that::cartoonCallback(int, void *) {
    cv::Mat imgMedian;
    cv::medianBlur(image, imgMedian, 7);

    cv::Mat imgCanny;
    cv::Canny(imgMedian, imgCanny, 60, 150);

    cv::Mat kernel = getStructuringElement(MORPH_RECT, Size(2, 2));
    cv::dilate(imgCanny, imgCanny, kernel);

    imgCanny= imgCanny / 255;
    imgCanny= 1 - imgCanny;

    cv::Mat imgCannyf;
    imgCanny.convertTo(imgCannyf, CV_32FC3);
    blur(imgCannyf, imgCannyf, Size(5,5));

    cv::Mat imgBF;
    cv::bilateralFilter(image, imgBF, 9, 150.0, 150.0);

    cv::Mat result = imgBF / 25;
    result = result * 25;

    cv::Mat imgCanny3c;
    cv::Mat cannyChannels[] = { imgCannyf, imgCannyf, imgCannyf };
    cv::merge(cannyChannels, 3, imgCanny3c);

    cv::Mat resultf;
    result.convertTo(resultf, CV_32FC3);
    multiply(resultf, imgCanny3c, resultf);
    resultf.convertTo(result, CV_8UC3);

    imshow("Result", result);
}