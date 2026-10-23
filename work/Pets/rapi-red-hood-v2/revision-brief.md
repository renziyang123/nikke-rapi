# 拉毗表情修订

用户认为旧版过于严肃，要求研究后期性格，并参考四张所附截图增加闷骚偷笑、坏笑、脸红和咬牙等表情。用户明确要求移除诡异跳跃。

保留稳定宠物 ID pet_6adb792197dc8191ba7a88a576da56cf，更新现有宠物，不新建。

保留已有左右跑动及十六方向视线的生成像素。修订 idle / waving / failed / waiting / running / review，原 jumping 五帧替换成双脚着地的掩嘴偷笑，肩部微颤、无跳起、无下蹲。用户要求优先于技能对跳跃语义的默认要求；不删除图集固定行，不伪造离地数据。最终质量检查对该明确取消的动作使用 --minimum-jump-lift 0，其他校验不变，并单独检查双脚基线。

来源：用户提供的四张表情截图为主要表情依据。
- https://www.bilibili.com/video/BV1NzQxBVE2L ：网页工具无法直接读取，未声称看过视频。
- https://nikke-goddess-of-victory-international.fandom.com/wiki/Rapi%3A_Red_Hood/Story ：社区整理，记录后期更活泼、会开玩笑、对指挥官更主动。
- https://game.udn.com/game/story/122089/8464792 ：报道个人花絮中主动索抱，相比以前更大胆。
- https://home.gamer.com.tw/artwork.php?sn=6081408 ：玩家整理关于后期活动与主线开玩笑/吐槽增多的观察，仅作辅助，不当作官方设定。

动作设计是新创作：待机轻笑眨眼，打招呼半眯眼勾嘴角，地面掩嘴偷笑，失败咬牙后别扭撅嘴，等待脸红绞手，工作专注检查背带后小得意，审阅托腮会心坏笑。保持原有成熟角色身份的Q版外形，不增加场景、文字、游离符号或新道具。

当前没有 ChatGPT Library 文件夹接口；所有本地材料和预览保存到此独立修订目录，并打包到 outputs/rapi-v2。
