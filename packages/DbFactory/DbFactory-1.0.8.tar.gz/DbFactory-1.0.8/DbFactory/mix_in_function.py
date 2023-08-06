# coding:utf-8
# author caturbhuja
# date   2020/9/11 11:22 上午 
# wechat chending2012 
import inspect

class MixInFunction:
    """"""    
    # --------------------------- 提示命令封装 -----------------------------
    def some_function(self, *args, **kwargs):
        """未来会定义的一些抽象方法"""
        return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)

    # ---------------------------- Mysql ---------------------------------
    # def select(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)
    #
    # def execute(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)




    def get(self, *args, **kwargs):
            """未来会定义的一些抽象方法"""
            return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)
