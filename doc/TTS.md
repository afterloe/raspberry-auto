# TTS实践
> create by [afterloe](605728727@qq.com)  
> version is 1.5  
> MIT License  


所用引擎为**Ekho(余音) - 中文语音合成软件**, 是一个免费、开源的中文语音合成软件。它目前支持粤语、普通话（国语）、广东台山话、
诏安客语、藏语、雅言（中国古代通用语）和韩语（试验中），英语则通过eSpeak或Festival间接实现。Ekho支持Linux、Windows和Android平台。此
平台的官网为: http://www.eguidedog.net/cn/ekho_cn.php。  
相关产品可以参考: http://www.eguidedog.net/index.php
## install
```shell script
sudo apt-get install apt-get install libsndfile1-dev libpulse-dev libncurses5-dev libmp3lame-dev libespeak-dev aplay -y
wget https://jaist.dl.sourceforge.net/project/e-guidedog/Ekho/8.0/ekho-8.0.tar.xz
tar -Jxvf ekho-8.0.tar.xz
cd ekho-8.0
su
./configure
make
make install
```

## tests
```shell script
ekho -h
Ekho text-to-speech engine.
Version: 8.0

Syntax: ekho [option] [text]
-v, --voice=VOICE
        Specified language or voice. ('Cantonese', 'Mandarin', 'Toisanese', 'Hakka', 'Tibetan', 'Ngangien' and 'Hangul' are available now. Mandarin is the default language.)
-l, --symbol
        List phonetic symbol of text. Characters' symbols are splited by space.
-f, --file=FILE
        Speak text file. ('-' for stdin)
-o, --output=FILE
        Output to file.
-t, --type=OUTPUT_TYPE
        Output type: wav(default), ogg or mp3
-p, --pitch=PITCH_DELTA
        Set delta pitch. Value range from -100 to 100 (percent)
-a, --volume=VOLUME_DELTA
        Set delta volume. Value range from -100 to 100 (percent)
-s, --speed=SPEED
        Set delta speed. Value range from -50 to 300 (percent)
--english-speed=SPEED
  Set English delta speed. Value range from -50 to 150 (percent)
--server
        Start Ekho TTS server.
--request=TEXT
        Send request to Ekho TTS server.
--port
        Set server port. Default is 2046.
--version
        Show version number.
-h, --help
        Display this help message.
```

## useage
```shell script
ekho "时间:10:20,车道:1,车牌:皖A51G61,违法代码:20004" -s -20 -o 123.wav
ekho "支付成功，消费%s圆" -s -30 -o voice.wav && aplay voice.wav
```

## summary

### 替换语音文件
1. 访问[Ekho Voice Data](访问Ekho Voice Data页面：https://sourceforge.net/projects/e-guidedog/files/Ekho-Voice-Data/0.2/)页面  
2. 找到需要下载的语言即版本，文件名中44100这样的数字表示音频文件的采样率，44100Hz是CD的音质。  
3. 下载后解压文件，并替换源码目录中Ekho/ekho-data文件夹里对应的语音数据文件夹。 如汉语为 pinyin  
4. 替换的为拼音或粤语，需要把ekho-data下的pinyin.voice和pinyin.index文件删除
5. 重启  
以上方法，同样适用于制作和替换自己的声音。

### 如何修订词典
对于发音不正确的多音字, 可以通过增加词条补丁来修正。方法如下:  
1. 编辑ekho-data/zh_patch, 模仿里面的格式修改。  
2. 删除ekho-data/zh.dict  
3. 运行ekho, zh.dict会被重新生成。第一次重新生成的时候会有一些报错信息, 如果报错信息和新增的修订无关可以忽略。否则, 请仔细检查。   

### 如何为Ekho添加新的声音
  请参看[链接](http://www.eguidedog.net/doc/doc_make_new_voice_cn.php)
  
### 二次开发
```cpp
/* file try.cpp */
#include "config.h" // this file is generated when building Ekho
#include "ekho.h"

using namespace ekho;

int main(int argc, char **argv) {
  Ekho wong("Cantonese");
  wong.blockSpeak("123");
  return 0;
}
```
.h文件可以在[这里](https://github.com/hgneng/ekho/blob/master/src/ekho.h)获取，Linux平台编译命令如下:
```shell script
g++ try.cpp libekho.a -pthread \
  -I. -Iutfcpp/source -Isonic -lsndfile \
  `pkg-config --libs libpulse-simple` `pkg-config --cflags libpulse-simple`
./a.out
```