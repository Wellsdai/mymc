# coding: utf-8
# 导入必要的库
import os, time
from mcpi.minecraft import Minecraft
import mcpi.block as block
import dashscope
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
os.environ.setdefault('DASHSCOPE_API_KEY',"sk-d7dd0437e3a5434a8ae87907eb74cce7")
dashscope.api_key=os.getenv('DASHSCOPE_API_KEY')


# 创建一个 Minecraft 实例
mc= Minecraft.create("127.0.0.1")

# 要监听的玩家的用户名
#target_player = "Adam2025"

# 聊天消息列表
chat_messages = []


#----------与人工智能对话模块-------------------
def conversation_with_GPT(message):
    while True:
        if len(chat_messages)>6:
            for i in range(2): chat_messages.pop(0)
            
        #message = input('user:')
        chat_messages.append({'role': Role.USER, 'content': message})
        response = Generation.call(Generation.Models.qwen_max, messages=chat_messages, result_format='message')
        rsp_msg = '小文:'+response.output.choices[0]['message']['content']
        print(rsp_msg)
        chat_messages.append({'role': response.output.choices[0]['message']['role'], 'content': response.output.choices[0]['message']['content']})
        print("message lengh:", len(chat_messages),chat_messages)
        return rsp_msg



#-------------自动建造建筑模块--------------
def build_structure():
    # 将玩家传送到原点
    #mc.player.setPos(0,0,0)
    # 获取玩家的当前位置
    player_pos = mc.player.getTilePos()
    print(player_pos.x,player_pos.y,player_pos.z,player_pos.x)
    # 获取玩家的当前朝向
    #player_dir = mc.player.getDirection()

    # 清空区域内的所有方块
    mc.setBlocks(player_pos.x,player_pos.y,player_pos.z,player_pos.x + 500,player_pos.y + 500,player_pos.z + 500,block.AIR.id)
    print("区域已清空！")


    # 定义房子的大小
    house_width = 10
    house_height = 8
    house_depth = 8

    # 定义房子的位置
    x = player_pos.x + 5
    y = player_pos.y
    z = player_pos.z + 5

    # 建造房子的墙壁
    print("开始建造墙壁")
    for i in range(house_height):
        for j in range(house_width):
            mc.setBlock(x + j, y + i, z, block.STONE.id)
            mc.setBlock(x + j, y + i, z + house_depth - 1, block.STONE.id)
            time.sleep(0.5)
        for k in range(house_depth):
            mc.setBlock(x, y + i, z + k, block.STONE.id)
            mc.setBlock(x + house_width -1, y + i, z + k, block.STONE.id)
            time.sleep(0.5)
        time.sleep(0.5)
            

    # 建造房子的屋顶
    print("开始建造屋顶")
    for i in range(house_width):
        for j in range(house_depth):
            mc.setBlock(x + i, y + house_height, z + j, block.WOOD.id)
            time.sleep(0.1)
        time.sleep(0.5)


    # 建造房子的窗户
    print("开始建造窗户")
    windows_width = house_width - 3
    windows_height = house_height //2

    #mc.setBlock(x + 1, y + 1, z, block.GLASS.id)
    mc.setBlocks(x + 1, y + 5, z, x + 1 + windows_width, y + 3 + windows_height, z, block.GLASS.id)

    # 建造房子的门
    print("开始建造大门")
    door_width = 2
    door_height = 3
    mc.setBlocks(x + house_width // 2 - door_width//2 -1 , y, z, x + house_width // 2 + door_width//2 , y + door_height, z, block.IRON_BLOCK)
    time.sleep(0.5)

    # 显示房子建造完成的信息
    print("房子建造完成！")



#-------------聊天模块--------------
def chat():
    # 主循环
    while True:
        # 获取最新的聊天消息
        # try:
        chat_events = mc.events.pollChatPosts()
        message =[]

        # 遍历聊天事件
        for chat_event in chat_events:
        
            # 检查消息是否来自目标玩家
            #if chat_event.entityId == mc.getPlayerEntityId(target_player):
            # 提取消息内容
            message = chat_event.message
            print(message)

            # 检查字符串是否以 "小文" 开头
            if message.startswith("小文"):
                # 提取出 "小文" 之后的字符串
                remaining_string = message[2:]
                # 去除剩余部分开头的逗号或者逗号
                remaining_string = remaining_string.lstrip('，,')
                print(remaining_string)
                mc.postToChat( "AI正在思考，请耐心等待。。。" )
                answer_msg = conversation_with_GPT(remaining_string)
                lines = str(answer_msg).splitlines()
                for line in lines:
                    if not line.isspace():mc.postToChat( line )
                    

            elif message=="建一座仓库":
                # print("开始建造教学楼")
                mc.postToChat("好的Adam，开始建造。。")
                build_structure()
        time.sleep(1)


if __name__ == '__main__':
    print('程序开始运行')
    mc.postToChat( "程序开始运行" )
    chat()


