<h1 align="center">LimbusCompany-IOS-Localization</h1>
<p align="center">
  边狱公司 IOS客户端 中文本地化
</p>
<p align="center">
  <a href=https://github.com/Ming900907/LimbusCompany-IOS-Localization/releases/latest><img src="https://img.shields.io/github/v/release/Ming900907/LimbusCompany-IOS-Localization?label=Version&style=for-the-badge" /></a>
  <a href=https://creativecommons.org/licenses/by-nc-sa/4.0><img src="https://img.shields.io/badge/Licence-CC_BY--NC--SA_4.0-blue?style=for-the-badge" /></a>
  <a href="https://t.me/+EqcZfY8aKAo1ZWE1"><img src="https://img.shields.io/badge/Telegram-group-blue?style=for-the-badge&logo=telegram&logoColor=white" /></a>
</p>
<p align="center">
  <a href=https://github.com/Ming900907/LimbusCompany-IOS-Localization><img src="https://img.shields.io/badge/dynamic/json?url=https://red-shadow-a504.ghcruise.workers.dev&query=$.json&label=Game%20Launches&logo=github&color=D4AF37&style=for-the-badge&cacheSeconds=60" /></a>
  <a href=https://github.com/Ming900907/LimbusCompany-IOS-Localization><img src="https://img.shields.io/badge/dynamic/json?url=https://red-shadow-a504.ghcruise.workers.dev&query=$.zip&label=Installs&logo=github&color=C0C0C0&style=for-the-badge&cacheSeconds=60" /></a>
  <a href=https://github.com/Ming900907/LimbusCompany-IOS-Localization><img src="https://img.shields.io/github/stars/Ming900907/LimbusCompany-IOS-Localization?label=Stars&logo=github&color=CD7F32&style=for-the-badge" /></a>
</p>

本文将介绍一种《边狱公司》（Limbus Company）iOS 的客户端汉化方案。   
适用于不想使用**Q公司**、**K公司**、**O公司**、**U公司**等加速器产品，且有其他代理工具的人群   

## 声明
- **前提：有其他代理工具（如Shadowrocket、Stash、~~Surge~~等）**
  - 如果您所在的地区有通畅的国际互联网连接，可以使用 Shadowrocket ，无需节点  
- 汉化资源来自 [LocalizeLimbusCompany](https://github.com/LocalizeLimbusCompany/LocalizeLimbusCompany)，遵循 [**CC BY-NC-SA 4.0 协议**](https://creativecommons.org/licenses/by-nc-sa/4.0/)   
- 包含战斗气泡，文本来自 [Bilibili调爪](https://space.bilibili.com/485880984)
- 关键词彩色高亮
- 剧情故事中的人物名和称号**完全汉化**
- 本项目将中文资源覆盖到游戏内**日语**语言槽位，因此需要在游戏中选择**日语**，以使用游戏内置的 CJK 字体并避免中文显示为方块
- 尚未汉化且存在英语对应项的文本会使用英文兜底；只有缺少英语对应项的少量资源会保留日文
- 由于IOS客户端字库限制，本项目在尽可能保留原意的前提下对汉化资源中的部分简体文本进行了替换  


## 原理简介
核心原理是通过 **中间人（Man-in-the-Middle）代理** 拦截游戏 API 返回的数据，并在返回客户端之前进行资源替换，从而实现翻译效果。  

[详细原理（施工中）]()
## 使用方法 
###  ！！必需！！ MitM配置 - CA证书安装 —— 以 Shadowrocket 为例
1. 打开Shadowrocket，进入`配置`页面，点击当前使用的规则最右侧的`ⓘ`进入`conf页面`
2. 进入`HTTPS解密`页面，启用`HTTPS解密`
3. 在弹出的证书页面选择`生成新的CA证书`并确认
4. 点击`安装证书`并允许下载描述文件
5. 在设备的`设置`→`通用`→`VPN与设备管理`页面选择下载的描述文件并安装
6. 在设备的`设置`→`通用`→`关于本机`→`证书信任设置`启用对安装证书的完全信任   

[另一份教程 （Shadowrocket）](https://github.com/LOWERTOP/Shadowrocket#https%E8%A7%A3%E5%AF%86)  
  
其他代理工具请参考各自工具的使用方法 **安装证书并开启Mitm**  

---
### 代理软件配置
安装 [Script-Hub 模块](https://github.com/Script-Hub-Org/Script-Hub/wiki/%E5%AE%89%E8%A3%85) 后，可点击下方链接导入：

- [Shadowrocket 直连+反代+IP优选](https://api.boxjs.app/shadowrocket/install?module=http%3A%2F%2Fscript.hub%2Ffile%2F_start_%2Fhttps%3A%2F%2Fraw.githubusercontent.com%2FMing900907%2FLimbusCompany-IOS-Localization%2Frefs%2Fheads%2Fmain%2FLimbusCompanyIOSLocalization-direct.module%2F_end_%2FLimbusCompanyIOSLocalization-direct.sgmodule%3Ftype%3Dsurge-module%26target%3Dshadowrocket-module%26del%3Dtrue%26jqEnabled%3Dtrue)

- [Shadowrocket 模块](https://api.boxjs.app/shadowrocket/install?module=http%3A%2F%2Fscript.hub%2Ffile%2F_start_%2Fhttps%3A%2F%2Fraw.githubusercontent.com%2FMing900907%2FLimbusCompany-IOS-Localization%2Frefs%2Fheads%2Fmain%2FLimbusCompanyIOSLocalization.module%2F_end_%2FLimbusCompanyIOSLocalization.sgmodule%3Ftype%3Dsurge-module%26target%3Dshadowrocket-module%26del%3Dtrue%26jqEnabled%3Dtrue)
  
- [Stash 覆写](https://api.boxjs.app/stash/install-override?url=http%3A%2F%2Fscript.hub%2Ffile%2F_start_%2Fhttps%3A%2F%2Fraw.githubusercontent.com%2FMing900907%2FLimbusCompany-IOS-Localization%2Frefs%2Fheads%2Fmain%2FLimbusCompanyIOSLocalization.module%2F_end_%2FLimbusCompanyIOSLocalization.stoverride%3Ftype%3Dsurge-module%26target%3Dstash-stoverride%26del%3Dtrue%26jqEnabled%3Dtrue)
  
- [Surge 模块](https://api.boxjs.app/surge/install-module?url=http%3A%2F%2Fscript.hub%2Ffile%2F_start_%2Fhttps%3A%2F%2Fraw.githubusercontent.com%2FMing900907%2FLimbusCompany-IOS-Localization%2Frefs%2Fheads%2Fmain%2FLimbusCompanyIOSLocalization.module%2F_end_%2FLimbusCompanyIOSLocalization.sgmodule%3Ftype%3Dsurge-module%26target%3Dsurge-module%26del%3Dtrue%26jqEnabled%3Dtrue&name=)

- [Loon 插件](https://www.nsloon.com/openloon/import?plugin=http%3A%2F%2Fscript.hub%2Ffile%2F_start_%2Fhttps%3A%2F%2Fraw.githubusercontent.com%2FMing900907%2FLimbusCompany-IOS-Localization%2Frefs%2Fheads%2Fmain%2FLimbusCompanyIOSLocalization.module%2F_end_%2FLimbusCompanyIOSLocalization.plugin%3Ftype%3Dsurge-module%26target%3Dloon-plugin%26del%3Dtrue%26jqEnabled%3Dtrue)
    


---
### 启动游戏
确认
- 启用VPN
- 启用上述配置  

资源下载
- **首次进入游戏会提示下载额外资源文件则说明汉化成功**
- **导入模块后汉化会随本项目自动更新，无需任何手动操作**

## 维护与发布
以原项目日语包为基础，用零协会仓库中的英语资源补齐尚未汉化的文件：

```bash
python3 tools/build_japanese_package.py localize_jp.zip manifest.json /path/to/LocalizeLimbusCompany
```

把生成的 `dist/localize_jp.zip` 和 `dist/manifest.json` 上传到同一个 Release。脚本会保留已有中文，使用英文替换零协会尚未提供中文的资源，并优化登录按钮和 Tips 标题。

## 最后
- 如果你觉得本项目对你有帮助，请帮忙点个 Star，这是对我最好的支持！
- ~~还不是为了自己在手机上玩得舒服，顺手搞的~~
- 对文本或其他方面有建议的可以在 Issue 中提出
- ~~最后还是建了个群~~ 欢迎入群：[Telegram 群组](https://t.me/+EqcZfY8aKAo1ZWE1)  

## 致谢
感谢都市零协会的无私付出:
https://github.com/LocalizeLimbusCompany/LocalizeLimbusCompany

Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
