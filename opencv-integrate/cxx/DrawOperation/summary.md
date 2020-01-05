# 绘图板
> create by [afterloe](605728727@qq.com)  
> MIT License  
> version 1.0  

源码看[这里](src/DrawOperation.cpp)

## 注意
### 填充
```
 -1, 8, 0 表示填充、实线
 1, 1, 0 表示虚线，空心

 eg:
 rectangle(image, rec1, Scalar(0,0,255), 1, 1, 0); // 虚线，空心矩形
```

### 文字
opencv的bug比较大，无法在图片上绘制中文，需要其他的函数库来实现。

## 资料
### 结构
```
DrawOperation
 - src
 ---- DrawOperation.cpp
 - CMakeLists.txt
```

### 源代码
```
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

    return 0;
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
```

### 编译
```
cmake_minimum_required(VERSION 2.8)
project( LearnOpencv )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( DrawOperation.out src/DrawOperation.cpp )
target_link_libraries( DrawOperation.out ${OpenCV_LIBS} )
```

### 执行
```
cmake .
make
./DrawOperation.out
```
