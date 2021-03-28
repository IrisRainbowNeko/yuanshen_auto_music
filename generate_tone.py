import mido
import numpy as np

input_path='./qby.mid'
output_path='./qby.ystone'

base_tone=48 # C3

tempo=500000

mid = mido.MidiFile(input_path, clip=True)

downsample_map=[0,0,1,1,2,3,3,4,4,5,5,6]

def note2click(note, last_note):
    clk_id = note-base_tone
    last_click = last_note-base_tone
    if clk_id<0 or clk_id>=12*3:
        raise Exception('音阶超出范围')
    clk_row=(clk_id//12)
    clk_col=downsample_map[clk_id%12]

    # 升降调优化策略1
    '''if (clk_id%12 in [1,3,6,8,10]) and ((last_click+1)%12 in [1,3,6,8,10]):
        if clk_row!=2 and clk_col!=6:
            clk_col+=1
            clk_row+=clk_col//7
            clk_col%=7

    if ((clk_id+1)%12 in [1,3,6,8,10]) and (last_click%12 in [1,3,6,8,10]):
        if clk_row!=0 and clk_col!=0:
            clk_col-=1
            clk_row+=clk_col//7
            clk_col%=7
    return [(clk_row, clk_col)]'''

    # 升降调优化策略2
    if clk_id%12 in [1, 3, 6, 8, 10]:
        return [(clk_row, clk_col),(clk_row, clk_col+1)] #模拟升降调
    else:
        return [(clk_row, clk_col)]

def track2group(track):
    tempo = 500000
    time_sum=0
    last_group=0
    groups=[]
    group_item=[]
    last_note=-1

    for msg in track:#每个音轨的消息遍历
        if msg.type=='set_tempo':
            tempo=msg.tempo
        print(msg, mido.tick2second(msg.time, mid.ticks_per_beat, tempo))
        time_sum+=mido.tick2second(msg.time, mid.ticks_per_beat, tempo)
        if msg.type=='note_on':
            group=time_sum
            if group<=last_group:
                group_item.extend(note2click(msg.note, last_note))
            else:
                if len(group_item)>0:
                    groups.append((last_group,group_item))
                group_item=note2click(msg.note, last_note)
            last_group=group
            last_note=msg.note
    groups.append((last_group, group_item))
    return groups

def group2blocks(group):
    blks=[]
    last_step=0
    for item in group:
        delays=('delay',item[0]-last_step)
        last_step = item[0]
        blks.append(delays)

        blks.append(('note',item[1]))
    return blks


for i, track in enumerate(mid.tracks):#enumerate()：创建索引序列，索引初始为0
    print(i)
    if i!=0:
        continue
    group=track2group(track)
    blks=group2blocks(group)
    script='\n'.join([str(x) for x in blks])
    print(script)
    with open(output_path, 'w') as f:
        f.write(script)