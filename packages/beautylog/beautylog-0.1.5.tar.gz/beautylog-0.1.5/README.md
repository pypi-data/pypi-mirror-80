Let your code generate logs automatically

# Version:0.0.1   
    2020/8/17 原始版本
# Version:0.0.2   
    2020/8/17 修正debug.log路径
# Version:0.0.3   
    2020/8/17 修正debug.log路径
# Version:0.0.5   
    2020/8/18 将函数中的print输出记录到日志中
# Version:0.1.0   
    2020/8/19

    1. 添加显示主函数对子函数调用关系的内容
    2. 兼容用户定义函数中存在try-expect语句的情况
    3. 将log修饰符从函数实现改为类实现
# Version:0.1.1   
    2020/9/2 skwood0105
    
    修复__BeautyLogOut__路径问题
# Version:0.1.2   
    2020/9/3 skwood0105
    
    增添判断调用是函数or方法的功能
    当所调用函数首参数是对象，且其中含有同名的类内成员函数时，无法判断（bug）
# Version:0.1.3   
    2020/9/5 Aglargil
    
    优化类内成员函数使用装饰器时log输出的内容
# Version:0.1.4   
    2020/9/5 skwood0105
    
    使用函数__qualname__属性判断调用是函数or方法，且解决了0.1.2中出现的bug
# Version:0.1.5  
    2020/9/9 Aglargil
    
    log定制化：
    1、可以指定某个函数的print输出是否需要改为定制输出（默认为需要）
    2、可以指定全部函数的print输出是否需要改为定制输出（默认为需要）

