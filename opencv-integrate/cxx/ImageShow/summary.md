# 图片展示
> create by [afterloe](605728727@qq.com)  
> MIT License  
> version 1.0  

## 注意事项
### CommandLineParser 的使用
CommandLineParser可以用于处理命令行参数，详细的可以查看[这里](https://docs.opencv.org/4.1.1/d0/d2e/classcv_1_1CommandLineParser.html)
```
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
```

### waitKey
waitKey 表示等待键盘输入，返回键位的code`char code = (char)cv::waitKey(int)`, int值表示等待时间
- 视频播放时，建议为每帧切换的时间
- 图片时，表示无限显示窗口
> cv::waitKey(int delay)函数用于显示的延迟。例如，waitKey(0)将无限显示窗口，直到按下任意按键退出延迟事件
（适用于显示图像）。如果delay大于0，例如，waitKey(25)将每隔至少25ms显示视频的一帧图像（适用于显示视频帧），如果要按键退出，则需要将waitKey(25)与一个按键值（ASCII码）比较。

### 资源释放
```
VideoCapture::release(); // 视频资源释放
Mat::release(); // 释放图片资源
cv::destroyAllWindows(); // 关闭所有窗口
```

## 资料
### 结构
```
ImageShow
 - src
 ---- ImageShow.cpp
 - CMakeLists.txt
```

### 源代码
```
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
```

### 编译
```
cmake_minimum_required(VERSION 2.8)
project( LearnOpencv )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( ImageShow.out src/ImageShow.cpp )
target_link_libraries( ImageShow.out ${OpenCV_LIBS} )
```

### 执行
```
cmake .
make
./ImageShow.out -src=path of image
```
