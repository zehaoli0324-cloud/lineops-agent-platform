from pathlib import Path
from html import escape
import json,base64,math,re,os,argparse
from PIL import ImageFont
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT.parent
TARGETS={'lineops-agent-platform':ROOT,'lineops-agentware-2026':ROOT.parent/'lineops-agentware-2026'}
FONT=os.getenv('LINEOPS_FIGURE_FONT','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');BOLD=os.getenv('LINEOPS_FIGURE_BOLD','/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
C={'ink':'#233344','muted':'#687582','line':'#C4CDD4','soft':'#F4F6F7','blue':'#3E668C','bluebg':'#EDF3F8','teal':'#258A82','tealbg':'#EAF5F1','purple':'#7A6B9D','purplebg':'#F1EEF7','amber':'#B98735','amberbg':'#FBF3E5','red':'#B66C65','redbg':'#FAEFED','white':'#FFFFFF'}
class Figure:
 def __init__(self,W=1820,H=1720):
  self.W=W;self.H=H;self.parts=[];self.nodes=[];self.links=[];self.textboxes=[]
  self.parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="figure-title figure-desc">')
  self.parts.append('<title id="figure-title">LineOps system architecture</title><desc id="figure-desc">Layered system architecture, causal feedback, explicit contracts and evidence boundaries. Status symbols distinguish software validation, partial integration and planned modules.</desc>')
  self.parts.append('<defs>'+''.join(f'<marker id="arr-{k}" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto" markerUnits="strokeWidth"><path d="M0 0 L7 3.5 L0 7 Z" fill="{C[k]}"/></marker>' for k in ['blue','teal','amber','muted','red','purple'])+'</defs>')
  self.rect(0,0,W,H,'white','none',0)
 def rect(self,x,y,w,h,fill='white',stroke='line',r=5,dash=None,sw=1.2):
  attrs=f' stroke-dasharray="{dash}"' if dash else ''
  self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{C.get(fill,fill)}" stroke="{C.get(stroke,stroke)}" stroke-width="{sw}"{attrs}/>')
 def line(self,pts,color='blue',dash=None,arrow=True,sw=2,label=None):
  d='M'+' L'.join(f'{x},{y}' for x,y in pts);attrs=f' stroke-dasharray="{dash}"' if dash else ''
  if arrow:attrs+=f' marker-end="url(#arr-{color})"'
  self.parts.append(f'<path d="{d}" fill="none" stroke="{C[color]}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"{attrs}/>')
  self.links.append({'points':pts,'color':color,'dash':dash})
 def text(self,x,y,t,size=20,color='ink',weight=400,anchor='start',width=None):
  if width:
   while ImageFont.truetype(BOLD if weight>500 else FONT,size).getlength(t)>width and size>13:size-=1
  t=escape(t)
  self.parts.append(f'<text x="{x}" y="{y}" fill="{C.get(color,color)}" font-family="Noto Sans CJK SC, Arial, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{t}</text>')
  self.textboxes.append((x,y,t,size))
 def dot(self,x,y,status='built',color='teal',r=5):
  self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{C[color]}" stroke-width="1.5" fill="{C[color] if status=="built" else C["white"]}"/>')
  if status=='partial':self.parts.append(f'<path d="M{x},{y-r} A{r},{r} 0 0 0 {x},{y+r} Z" fill="{C[color]}"/>')
 def node(self,id,x,y,w,h,title,subtitle='',tiny='',color='blue',status='built',detail=''):
  self.parts.append(f'<g class="module" id="mod-{id}" data-status="{status}" data-detail="{escape(detail or subtitle)}" tabindex="0" role="button" aria-label="{escape(title+": "+subtitle)}">')
  self.rect(x,y,w,h,color+'bg',color,5,sw=1.1)
  self.dot(x+w-14,y+15,status,color,4)
  self.text(x+15,y+29,title,20,color='ink',weight=600,width=w-42)
  if subtitle:self.text(x+15,y+54,subtitle,16,color='muted',width=w-28)
  if tiny:self.text(x+15,y+h-13,tiny,14,color='muted',width=w-28)
  self.parts.append('</g>');self.nodes.append({'id':id,'title':title,'subtitle':subtitle,'status':status,'detail':detail or subtitle,'bounds':[x,y,w,h]})
 def panel(self,letter,title,subtitle,x,y,w,h):
  self.rect(x,y,w,h,'white','line',0,sw=1)
  self.text(x+20,y+34,letter,29,weight=700)
  self.text(x+55,y+32,title,24,weight=600,width=w-75)
  if subtitle:self.text(x+55,y+57,subtitle,16,color='muted',width=w-74)
 def lane(self,x,y,w,h,num,title,sub):
  self.rect(x,y,w,h,'soft','none',4)
  self.text(x+14,y+(16 if h<80 else 24),num,12,color='muted',weight=700)
  self.text(x+14,y+(37 if h<80 else 53),title,17,weight=600,width=156)
  if h>=80:self.text(x+14,y+77,sub,14,color='muted',width=160)
 def label(self,x,y,t,color='muted',size=14,anchor='middle'):
  font=ImageFont.truetype(FONT,size);w=font.getlength(t)+12
  self.rect(x-w/2,y-size+1,w,size+7,'white','none',2)
  self.text(x,y,t,size,color=color,anchor=anchor)
 def image(self,x,y,w,h,png):
  self.parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(png).decode()}"/>')
 def finish(self):return ''.join(self.parts)+'</svg>'

def header(f,title,subtitle,statusnote):
 f.text(44,55,'LINEOPS',17,color='blue',weight=700)
 f.text(44,100,title,37,weight=600)
 f.text(45,133,subtitle,19,color='muted')
 f.text(1774,55,'SYSTEM DESIGN / 2026.11',14,color='muted',anchor='end')
 f.text(1774,78,statusnote,14,color='muted',anchor='end')

def legend(f,y):
 f.line([(48,y),(90,y)],'teal');f.text(102,y+5,'Observation / evidence  数据与证据',15)
 f.line([(445,y),(487,y)],'blue');f.text(499,y+5,'Dispatch / query  编排与查询',15)
 f.line([(837,y),(879,y)],'amber');f.text(891,y+5,'State mutation  状态变更',15)
 f.line([(1195,y),(1237,y)],'muted',dash='5 5');f.text(1249,y+5,'Offline evaluation  离线评测',15)
 f.dot(54,y+35,'built');f.text(67,y+40,'Software tested  软件已测',14,color='muted')
 f.dot(361,y+35,'partial');f.text(374,y+40,'Partial / protocol only  部分接入',14,color='muted')
 f.dot(730,y+35,'planned');f.text(743,y+40,'Planned  规划',14,color='muted')
 f.text(1774,y+40,'Colour encodes function; symbols encode maturity.',14,color='muted',anchor='end')

def full():
 f=Figure(1820,1780)
 header(f,'Modular industrial maintenance agent platform','Layered orchestration, causal intervention and verifiable recovery','FULL PLATFORM · v0.1 + ROADMAP')
 f.panel('a','Layered system architecture','Seven planes share contracts; adapters isolate equipment-specific semantics.',44,173,1190,1068)
 x=66;w=1146;xs=[250,550,850];ws=[280,280,340];cx=[390,690,1020]
 lanes=[(255,99,'01','Experience','工作台与人机接口'),(383,131,'02','Runtime control','生命周期与约束'),(551,115,'03','Agent reasoning','诊断、规划与验证'),(703,112,'04','Tool boundary','工具权限与执行'),(853,113,'05','Data & compute','感知、后端与证据'),(1003,99,'06','Adapter layer','采集与业务适配'),(1136,82,'07','World & business','真实或虚拟产线')]
 for y,h,n,t,s in lanes:f.lane(x,y,w,h,n,t,s)
 # Main edges drawn before modules and routed in dedicated gutters.
 f.line([(390,341),(390,367),(1020,367),(1020,341)],'blue',arrow=False)
 f.line([(690,341),(690,393)],'blue');f.label(770,381,'requests / state',size=13)
 f.line([(690,514),(690,535)],'blue',arrow=False)
 f.line([(390,535),(1020,535)],'blue',arrow=False)
 for c in cx:f.line([(c,535),(c,562)],'blue')
 for c in cx:f.line([(c+18,650),(c+18,717)],'blue')
 f.label(738,691,'bounded tool calls',size=13)
 # Observation chain upward, separate from action path.
 f.line([(365,1147),(365,1090)],'teal')
 f.line([(665,1147),(665,1110),(345,1110),(345,1090)],'teal')
 f.line([(365,1014),(365,953)],'teal')
 f.line([(365,864),(365,800)],'teal')
 f.line([(365,717),(365,650)],'teal')
 f.line([(408,800),(408,864)],'blue')
 f.line([(408,953),(408,1014)],'blue')
 f.label(452,987,'read / sample',size=12)
 # State mutation bypasses inference; it never flows "through" the model backend.
 f.line([(748,800),(748,830),(840,830),(840,1048),(830,1048)],'amber')
 f.label(839,986,'execute',color='amber',size=12)
 f.line([(690,1090),(690,1120),(390,1120),(390,1136)],'amber')
 f.line([(690,1120),(690,1136)],'amber')
 # CPU / optical capability route, evidence access, business.
 f.line([(530,894),(550,894)],'blue')
 f.line([(830,926),(850,926)],'teal')
 f.line([(1020,853),(1020,800)],'teal')
 f.line([(1020,1090),(1020,1136)],'amber')
 f.line([(1020,1003),(1020,953)],'teal')
 # Right data spine carries fresh evidence to verifier and runtime.
 f.line([(1190,903),(1199,903),(1199,610),(1190,610)],'teal')
 f.line([(1199,610),(1199,449),(1190,449)],'teal')
 f.label(1197,693,'fresh evidence',color='teal',size=12)
 # Interface plane
 f.node('fuxa',250,266,280,75,'FUXA HMI','设备图 / 标签 / 趋势',color='blue',status='planned',detail='FUXA 源码已固定。实际部署、画面配置与 MQTT 标签绑定尚未完成，初期只读。')
 f.node('console',550,266,280,75,'Evidence console','图像 / 事件 / 工具轨迹',color='blue',detail='已实现独立浏览器证据页，展示运行模式、动作前后 PNG、事件终态、工单和轨迹。')
 f.node('portal',850,266,340,75,'Maintenance portal','人工接管 / 审批 / 资源视图',color='blue',status='planned',detail='规划：工单门户、人工接管与资源视图。当前仅内置测试工单，不是外部 CMMS。')
 # Runtime outer container hierarchy.
 f.rect(238,393,964,111,'white','blue',5)
 f.text(254,417,'DETERMINISTIC OPERATIONS MANAGER',14,'blue',600)
 f.node('lifecycle',250,428,280,65,'Incident lifecycle','终态 / 工单 / 审计',color='blue',detail='已测试 created → running → recovered / handed_off / stopped / failed；SQLite 保存事件、PNG 与工单。')
 f.node('budgets',550,428,280,65,'Budgets & stop','步数限额 / 单进程锁',color='blue',detail='已实现工具调用预算、单进程设备锁、停止标记。未实现跨进程锁或多设备调度。')
 f.node('scheduler',850,428,340,65,'Queue & checkpoint','租约 / 健康 / 重启恢复',color='blue',status='planned',detail='规划：异步队列、租约、心跳与世界检查点。当前重启后未完成任务标 failed，不能接续执行。')
 for id,c,title,sub in [('diagnosis',250,'Diagnostic agent','取证 / 比较候选原因'),('planner',550,'Planning agent','方案 / 允许动作 / 移交'),('verifier',850,'Verification agent','新观测 / 恢复判定')]:
  f.node(id,c,562,280 if c!=850 else 340,88,title,sub,'Shared tool-calling LLM interface',color='purple',status='partial',detail='角色权限与工具调用协议 mock 已测；尚无真实模型效果记录。三角色共享模型端点，由确定性运行器编排。')
 f.node('readtools',250,717,280,83,'Observation tools','图像 / 遥测 / 内置手册',color='teal',detail='Agent 仅读取公开观测、像素测量、遥测与手册，工具不返回隐藏故障标签。')
 f.node('gateway',550,717,280,83,'Action gateway','白名单 / 版本 / TTL / 幂等',color='amber',detail='已测试维护前暂停、陈旧版本、过期与非有限有效期、非法动作和重复动作 ID；重放不重复变更状态。')
 f.node('recovery',850,717,340,83,'Recovery evaluator','新帧 / 质量 / 过程 / 运行态',color='teal',detail='固定代码强制三次新帧复核。模型结论与工具成功回执均不能直接标记 recovered；目前没有物理时间稳定窗口。')
 f.node('perception',250,864,280,89,'Perception adapters','测量 / 分割 / 信号特征','v0.1: synthetic RGB measurement',color='teal',status='partial',detail='当前从合成 PNG 使用 RGB 阈值测量胶条覆盖率与液位，未训练工业模型；其他视觉与信号插件属于规划。')
 f.node('compute',550,864,280,89,'Compute dispatcher','CPU / optical / GPU','Neuroptica: standalone check',color='teal',status='partial',detail='CPU 像素测量已测。Neuroptica 8 端口功能单测通过，尚未进入视觉决策链；GPU 和真实硬件后端为规划。')
 f.node('evidence',850,864,340,89,'Evidence & memory','PNG / 测量 / 回执 / 案例','SQLite audit; knowledge retrieval later',color='teal',status='partial',detail='SQLite 已保存事件、不可变 PNG、工具参数与回执、工单。知识检索与跨任务记忆管理待实现。')
 f.node('readadapters',250,1014,280,76,'Sensor readers','相机 / PLC / MQTT / 日志',color='teal',status='partial',detail='模拟器图像和供压适配已实现；实际 PLC、相机、视频和 MQTT 传输未接入。')
 f.node('actadapters',550,1014,280,76,'Actuator adapters','暂停 / 维护 / 恢复 / 查询',color='amber',status='partial',detail='目前仅执行软件沙箱动作。真实设备写入需要独立设备语义、权限、质量和验收。')
 f.node('businessadapters',850,1014,340,76,'Business connectors','CMMS / 备件 / 人员 / 排程',color='amber',status='planned',detail='外部业务系统与资源排程为规划；当前测试工单存储于内部 SQLite。')
 f.node('virtual',250,1147,280,60,'Virtual production line','点胶 / 灌装；有状态因果',color='teal',detail='两场景 × 五条件已测：正常、堵塞、供料不足、镜头退化、持续故障。仅简化离散软件模型。')
 f.node('physical',550,1147,280,60,'Physical equipment','真实设备 / 多模态采集',color='teal',status='planned')
 f.node('business',850,1147,340,60,'Business systems','工单 / 资源 / 维护窗口',color='amber',status='planned')
 # Closed-loop inset
 f.panel('b','Intervene, then verify','A successful action receipt is not recovery.',1280,173,496,1068)
 yy=[266,390,516,642,768,894,1020];cc=['teal','purple','purple','amber','amber','teal','teal']
 labels=[('01','Observe','补采图像与过程数据'),('02','Form hypotheses','根据证据比较故障原因'),('03','Choose intervention','比较检查、维护与移交'),('04','Check preconditions','状态版本 / 有效期 / 暂停'),('05','Mutate plant state','执行后取得真实工具回执'),('06','Acquire fresh evidence','重新渲染 / 重新测量'),('07','Evaluate recovery','固定规则判定；不得自报成功')]
 for i,(n,t,sub) in enumerate(labels):
  if i:f.line([(1528,yy[i-1]+86),(1528,yy[i])], 'amber' if i in [3,4] else 'teal')
  f.node('loop-'+n,1320,yy[i],416,86,n+'  '+t,sub,color=cc[i],status='built' if i not in [1,2] else 'partial')
 # Return loops in outer margins, not through node labels.
 f.line([(1736,1060),(1755,1060),(1755,559),(1736,559)],'blue')
 f.label(1528,1133,'terminal policy',color='muted',size=14,anchor='middle')
 f.line([(1528,1106),(1528,1148)],'teal',arrow=False)
 f.line([(1387,1148),(1687,1148)],'teal',arrow=False)
 for c in [1387,1537,1687]:f.line([(c,1148),(c,1163)],'teal')
 for x0,title,color in [(1314,'Recovered','teal'),(1464,'Handed off','amber'),(1614,'Stopped / failed','muted')]:
  f.rect(x0,1163,146,42,C.get(color+'bg','soft'),color,4);f.text(x0+73,1190,title,15,color=color,weight=600,anchor='middle')
 # Compatibility matrix, with stable seam separated from plugins.
 f.panel('c','Compatibility through stable interfaces','Reuse the control core; implement and validate each adapter.',44,1282,1190,350)
 cols=[(68,348,'SCENARIO', 'glue · filling', 'new line: render + causal actions'),(444,348,'SENSING TASK','RGB measurement', 'thermal · vibration · 3D: planned'),(820,390,'COMPUTE BACKEND','CPU · optical function check','GPU / physical chip: planned')]
 for x0,ww,t,a,b in cols:
  f.rect(x0,1366,ww,110,'soft','line',4);f.text(x0+16,1392,t,14,color='blue',weight=700);f.text(x0+16,1423,a,20,weight=600,width=ww-30);f.text(x0+16,1451,b,15,color='muted',width=ww-30)
  f.line([(x0+ww/2,1476),(x0+ww/2,1506)],'blue')
 f.rect(68,1506,1142,94,'bluebg','blue',5)
 f.text(86,1533,'SHARED CONTRACTS',14,color='blue',weight=700)
 f.text(86,1561,'Observation → Measurement → Action → Receipt → Verification',22,weight=600,width=1100)
 f.text(86,1586,'Identity · timestamps · quality · units · state version · provenance · terminal criteria',15,color='muted')
 # Firewall and offline evaluation.
 f.panel('d','Evidence boundary','Fault truth belongs to evaluation, not Agent tools.',1280,1282,496,350)
 f.node('truth',1302,1372,145,83,'Hidden truth','故障 / 种子',color='red',detail='私有真值供模拟器与评测端使用，不作为 Agent 的工具输出。')
 f.node('render',1464,1372,127,83,'Renderer','状态 → 观测',color='teal')
 f.node('publicobs',1608,1372,145,83,'Public data','PNG / 遥测',color='teal')
 f.line([(1447,1413),(1464,1413)],'teal');f.line([(1591,1413),(1608,1413)],'teal')
 f.line([(1374,1455),(1374,1498)],'muted',dash='5 5')
 f.line([(1680,1455),(1680,1498)],'muted',dash='5 5')
 f.rect(1302,1498,451,92,'soft','line',4)
 f.text(1320,1527,'Offline evaluator',20,weight=600)
 f.text(1320,1553,'truth + actions + terminal evidence',16,color='muted')
 f.text(1320,1577,'10 baseline tasks; not field coverage',15,color='muted')
 legend(f,1675)
 f.text(46,1752,'Fig. 1 | Architecture and validation boundary of the full LineOps platform. Symbols refer to current software maturity, not physical deployment.',16,color='muted')
 return f

def competition():
 f=Figure(1820,1695)
 header(f,'Autonomous night-shift incident response','A bounded Agent task with tool execution, causal feedback and inspectable outcomes','AGENTWARE · DESIGN ONLY BEFORE KICKOFF')
 f.panel('a','Task-oriented Agent architecture','P0 = one autonomous glue-line incident; P1 = adapter and backend tests.',44,173,1190,746)
 for y,h,n,t,s in [(255,100,'01','Task envelope','异常 / 目标 / 预算'),(399,100,'02','Coordinator','状态 / 权限 / 停止'),(543,119,'03','Agent roles','按职责调用同一模型'),(706,102,'04','Tool contract','读取 / 执行 / 复核'),(846,52,'05','Deliverable','可核实终态与轨迹')]:
  f.lane(66,y,1146,h,n,t,s)
 xs=[250,550,850];cx=[390,690,1020]
 f.line([(390,341),(390,374),(1020,374),(1020,341)],'blue',arrow=False)
 f.line([(690,341),(690,410)],'blue')
 f.line([(690,486),(690,522)],'blue',arrow=False);f.line([(390,522),(1020,522)],'blue',arrow=False)
 for c in cx:f.line([(c,522),(c,555)],'blue')
 for c in cx:f.line([(c,646),(c,718)],'blue')
 f.label(756,688,'bounded tool calls',size=14)
 f.line([(365,718),(365,646)],'teal')
 f.line([(1020,795),(1020,857)],'teal')
 f.node('event',250,266,280,75,'Incident event','设备身份 / 时间 / 异常',color='teal',status='planned')
 f.node('objective',550,266,280,75,'Goal & constraints','恢复或移交；明确终态',color='blue',status='planned')
 f.node('ui',850,266,340,75,'FUXA + evidence UI','只读产线图 / 工具与图像证据',color='blue',status='planned')
 f.rect(238,410,964,76,'bluebg','blue',5)
 f.text(254,438,'OPERATIONS COORDINATOR',19,weight=600)
 f.text(254,465,'Incident state · role permissions · call budget · action receipts · stop switch · audit',16,color='muted',width=920)
 for id,x,w,title,sub in [('diag',250,280,'Diagnostic role','补证据 / 比较假设'),('plan',550,280,'Planning role','选择工具 / 处置或移交'),('verify',850,340,'Verification role','新观测 / 判定与解释')]:
  f.node(id,x,555,w,91,title,sub,'One model endpoint; restricted tool sets',color='purple',status='planned')
 f.node('read',250,718,280,77,'Observe / query','图像测量 / 供压 / 手册',color='teal',status='planned')
 f.node('act',550,718,280,77,'Act / open work order','暂停 → 维护 → 恢复',color='amber',status='planned')
 f.node('check',850,718,340,77,'Verify fresh observations','质量 / 测量阈值 / 运行状态',color='teal',status='planned')
 f.rect(250,857,940,30,'tealbg','teal',3);f.text(270,879,'Terminal result + before/after PNG + tool trace + work order, if unresolved',16,color='teal')
 # Tool layer to sandbox via dedicated gap, with read vs mutation clearly separated.
 f.line([(690,795),(690,825),(1247,825),(1247,817),(1310,817)],'amber')
 f.label(1140,818,'allowed action',color='amber',size=12)
 f.line([(1310,701),(1254,701),(1254,699),(390,699),(390,718)],'teal')
 f.label(1121,688,'new observation',color='teal',size=12)
 f.panel('b','Causal software sandbox','State generates evidence; actions change state.',1280,173,496,746)
 f.node('hidden',1310,266,436,64,'Private fault injection','操作者选择；Agent 工具不可见',color='red',status='planned')
 f.line([(1528,330),(1528,369)],'muted',dash='5 5')
 f.node('state',1310,369,436,82,'Authoritative plant state','供料 / 喷嘴 / 镜头 / 运行状态',color='teal',status='planned')
 f.line([(1528,451),(1528,478)],'teal',arrow=False);f.line([(1414,478),(1642,478)],'teal',arrow=False)
 for c in [1414,1642]:f.line([(c,478),(c,505)],'teal')
 f.node('frame',1310,505,208,87,'Image renderer','胶条 / 液位 PNG',color='teal',status='planned')
 f.node('telemetry',1538,505,208,87,'Process telemetry','供压 / 设备运行态',color='teal',status='planned')
 f.line([(1414,592),(1414,626),(1528,626)],'teal',arrow=False)
 f.line([(1642,592),(1642,626),(1528,626),(1528,662)],'teal')
 f.line([(1300,646),(1756,646)],'muted',dash='3 5',arrow=False,sw=1)
 f.label(1530,642,'AGENT-VISIBLE BOUNDARY',size=12)
 f.node('observations',1310,662,436,78,'Observation bundle','frame_id / version / quality / telemetry',color='teal',status='planned')
 f.node('statechange',1310,782,436,71,'Action changes world','有效动作才改变状态；错误维修可无效',color='amber',status='planned')
 f.line([(1746,817),(1761,817),(1761,410),(1746,410)],'amber')
 f.text(1315,889,'Glue = main demo    Filling = compatibility test',16,color='muted')
 # State machine, explicit terminal logic.
 f.panel('c','Bounded execution and failure handling','Every run ends in an evidenced outcome; tool success alone is insufficient.',44,965,1190,554)
 f.node('created',80,1067,170,69,'Created','事件进入',color='blue',status='planned')
 f.node('running',350,1067,235,69,'Running','取证 / 规划 / 执行',color='purple',status='planned')
 f.node('verifying',730,1067,235,69,'Verifying','采集新证据 / 检查',color='teal',status='planned')
 f.node('recovered',1040,1067,162,69,'Recovered','证据支持恢复',color='teal',status='planned')
 f.line([(250,1102),(350,1102)],'blue');f.line([(585,1102),(730,1102)],'blue');f.line([(965,1102),(1040,1102)],'teal')
 f.label(661,1086,'post-action',size=13);f.label(1002,1086,'pass',color='teal',size=13)
 f.line([(792,1136),(792,1206),(520,1206),(520,1136)],'blue')
 f.label(652,1197,'not restored + retry budget',color='blue',size=14)
 f.node('stopped',350,1340,235,72,'Stopped','预算耗尽 / 人工停止',color='blue',status='planned')
 f.node('handoff',730,1340,235,72,'Handed off','未解决 + 已暂停 + 工单',color='amber',status='planned')
 f.node('failed',1040,1340,162,72,'Failed','协议或工具异常',color='red',status='planned')
 f.line([(412,1136),(412,1340)],'blue');f.label(414,1274,'budget / stop',size=13,color='blue')
 f.line([(900,1136),(900,1275),(847,1275),(847,1340)],'amber');f.label(933,1256,'handoff conditions',size=13,color='amber')
 f.line([(467,1067),(467,1048),(1215,1048),(1215,1376),(1202,1376)],'red');f.label(1153,1290,'unhandled error',size=12,color='red')
 f.rect(80,1445,1122,49,'soft','line',3)
 f.text(98,1475,'Action gate: allowlist + fresh version + TTL + maintenance pause + idempotency',18,weight=500,width=1080)
 # Evidence bundle: real baseline thumbnails, explicitly design examples.
 f.panel('d','Inspect the evidence','Illustrative synthetic frames; no competition result claimed.',1280,965,496,554)
 import sys
 sys.path.insert(0,str(ROOT))
 from lineops.simulator import World
 _,before=World('glue','clog').capture();_,after=World('glue','normal').capture()
 f.image(1302,1054,210,118,before);f.image(1542,1054,210,118,after)
 f.text(1302,1196,'Before intervention',15,color='muted');f.text(1542,1196,'After effective repair',15,color='muted')
 f.line([(1508,1110),(1541,1110)],'amber')
 f.text(1302,1245,'REQUIRED OUTPUTS',14,color='blue',weight=700)
 for i,(a,b) in enumerate([('01','Before / after frame IDs and measurements'),('02','Actual tool arguments and receipts'),('03','Recovery predicate or unresolved evidence'),('04','Replayable trace, tests and demo video')]):
  y=1279+i*43;f.text(1302,y,a,14,color='muted',weight=600);f.text(1335,y,b,16,width=415)
 f.text(1302,1487,'CPU path first; optical small task is P1.',16,color='muted')
 legend(f,1570)
 f.text(46,1651,'Fig. 2 | Competition scope: autonomous glue-line triage, intervention and verification; adapter and optical extensions follow only after the P0 workflow is reliable.',16,color='muted')
 return f

STYLE='''*{box-sizing:border-box}body{margin:0;background:#f0f2f4;color:#233344;font:15px/1.7 system-ui,"Noto Sans CJK SC",sans-serif}header,.wrap,footer{max-width:1580px;margin:auto;padding:24px 34px}header{padding-top:40px}h1{font-size:29px;font-weight:600;letter-spacing:-.6px;margin:10px 0}header p{max-width:980px;color:#697581;margin:8px 0}.eyebrow{font-size:12px;letter-spacing:1.8px;color:#3e668c;font-weight:700}nav{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0}button,.link{appearance:none;background:white;border:1px solid #bfc9d1;border-radius:3px;padding:8px 15px;font:inherit;cursor:pointer;color:#31495f;text-decoration:none}button[aria-pressed=true]{background:#233b52;color:white;border-color:#233b52}button:focus-visible,.module:focus-visible{outline:3px solid #b98735;outline-offset:3px}.stage{background:white;border:1px solid #d4dbe0;overflow:auto}.viewport{min-width:900px;transform-origin:top left}.viewport svg{display:block;width:100%;height:auto}.module{cursor:pointer}.module:hover rect{stroke-width:2.4}.module.focused rect{stroke-width:2.8}.dim{opacity:.18}.trace-data path:not([stroke="#258A82"]),.trace-control path:not([stroke="#3E668C"]),.trace-action path:not([stroke="#B98735"]){opacity:.12}.guide{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:18px}.note{background:white;border:1px solid #d4dbe0;padding:20px}.note h2{margin:0 0 8px;font-size:17px}.note p{margin:6px 0;color:#5b6d7c}.caption{font-size:14px;color:#5b6d7c;margin:18px 0}#detail{border-left:3px solid #7a6b9d}select{font:inherit;padding:8px}.status{font-size:13px;color:#3e668c}a{color:#3e668c}footer{font-size:12px;color:#687582}.screenhint{font-size:12px;color:#687582}@media(max-width:800px){header,.wrap,footer{padding:18px}h1{font-size:23px}.guide{grid-template-columns:1fr}.viewport{min-width:1120px}.stage{max-height:78vh}.screenhint{display:block}}@media print{body{background:white}header,footer,nav,.guide,.screenhint{display:none}.wrap{max-width:none;padding:0}.stage{border:0;overflow:visible}.viewport{min-width:0!important;width:100%!important}.viewport svg{width:100%} .caption{font-size:8pt} @page{size:A3 portrait;margin:12mm}}'''
JS='''const figure=document.querySelector('svg'),view=document.getElementById('view');const defaultText=document.getElementById('detail').innerHTML;function selectModule(el){document.querySelectorAll('.module').forEach(g=>g.classList.toggle('focused',g===el));const data=modules.find(m=>'mod-'+m.id===el.id);if(!data)return;const d=document.getElementById('detail');d.replaceChildren();const h=document.createElement('h2');h.textContent=data.title;const p=document.createElement('p');p.textContent=data.detail;const s=document.createElement('p');s.className='status';s.textContent={built:'当前软件路径已测试',partial:'部分接入或协议已测；详见说明',planned:'设计目标，尚未验证'}[data.status];d.append(h,p,s)}document.querySelectorAll('.module').forEach(el=>{el.onclick=()=>selectModule(el);el.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectModule(el)}}});document.querySelectorAll('[data-flow]').forEach(b=>b.onclick=()=>{figure.classList.remove('trace-data','trace-control','trace-action');if(b.dataset.flow!=='all')figure.classList.add('trace-'+b.dataset.flow);document.querySelectorAll('[data-flow]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))});document.getElementById('maturity').onclick=e=>{const active=e.currentTarget.getAttribute('aria-pressed')!=='true';e.currentTarget.setAttribute('aria-pressed',String(active));document.querySelectorAll('.module').forEach(el=>el.classList.toggle('dim',active&&el.dataset.status==='planned'))};document.getElementById('zoom').onchange=e=>{view.style.width=e.target.value==='fit'?'100%':e.target.value+'px'};document.getElementById('print').onclick=()=>window.print();document.getElementById('reset').onclick=()=>{figure.classList.remove('trace-data','trace-control','trace-action');document.querySelectorAll('.module').forEach(el=>el.classList.remove('dim','focused'));document.getElementById('detail').innerHTML=defaultText;document.getElementById('maturity').setAttribute('aria-pressed','false');document.querySelectorAll('[data-flow]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.flow==='all')))};'''

def export(name,fig,number,caption,panelguide):
 d=TARGETS[name]/'docs';d.mkdir(parents=True,exist_ok=True);svg=fig.finish();svgname='architecture-full.svg' if name.endswith('platform') else 'architecture-competition.svg'
 (d/svgname).write_text(svg)
 title='完整平台：分层、适配与验证架构' if name.endswith('platform') else '比赛版本：自主处置与故障反馈架构'
 maturity='完整平台 v0.1：已测、部分接入与规划分别标记。' if name.endswith('platform') else '比赛项目赛前仅设计；图中状态全部为规划。示例图像来自完整项目模拟器，不是参赛结果。'
 page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{STYLE}</style></head><body><header><span class="eyebrow">LINEOPS / FIGURE {number} / SYSTEM ARCHITECTURE</span><h1>{title}</h1><p>按论文多面板系统图重新组织。层级、因果与接口分别表达；颜色区分流的语义，状态符号区分当前实现与后续目标。</p><p class="status">{maturity}</p><nav aria-label="图表控制"><button data-flow="all" aria-pressed="true">全部关系</button><button data-flow="data" aria-pressed="false">数据与证据流</button><button data-flow="control" aria-pressed="false">编排与查询流</button><button data-flow="action" aria-pressed="false">状态变更流</button><button id="maturity" aria-pressed="false">突出当前软件能力</button><button id="reset">还原</button><select id="zoom" aria-label="缩放"><option value="fit">适应页面</option><option value="1820">100% 放大</option><option value="2400">细节放大</option></select><button id="print">打印</button><a class="link" href="{svgname}" download>SVG 矢量图</a><a class="link" href="{svgname[:-4]}.pdf" download>PDF</a></nav><p class="screenhint">点击模块查看边界与实现说明。手机可横向滑动图面；SVG 和 PDF 适合放大、排版与继续编辑。</p></header><main class="wrap"><div class="stage"><div class="viewport" id="view">{svg}</div></div><p class="caption"><strong>图 {number}.</strong> {caption}</p><div class="guide"><section class="note"><h2>阅读顺序</h2>{panelguide}</section><section class="note" id="detail" aria-live="polite"><h2>模块与证据说明</h2><p>点击图内模块查看职责、依赖和当前实现状态。实心表示对应软件路径已测试；半实心表示部分接入或仅协议验证；空心表示规划。</p><p>图示采用平面矢量、多面板、有限配色与显式边界，未暗示已获得期刊认可或满足某一期刊的最终排版要求。</p></section></div></main><footer>2026-11-16 · 原生 HTML + 内联 SVG；无外部脚本、图片或字体下载。图内示例是软件模拟；不代表真实工业部署或光学芯片性能。<a href="PROPOSAL.html">Proposal</a> · <a href="SPECIFICATION.md">实施规格</a></footer><script>const modules={json.dumps(fig.nodes,ensure_ascii=False)};{JS}</script></body></html>'''
 (d/'architecture.html').write_text(page)
 # Source and metadata for reproducible editing; full repo builder later copied separately.
 (d/'architecture-layout.json').write_text(json.dumps({'figure':number,'canvas':[fig.W,fig.H],'nodes':fig.nodes,'links':fig.links,'caption':caption},ensure_ascii=False,indent=2)+'\n')
 import cairosvg
 cairosvg.svg2png(bytestring=svg.encode(),write_to=str(d/svgname.replace('.svg','.png')),output_width=2184)
 cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(d/svgname.replace('.svg','.pdf')))
 print(json.dumps({'name':name,'modules':len(fig.nodes),'connections':len(fig.links),'html_bytes':len(page.encode())}))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--project',choices=['full','competition','both'],default='full');parser.add_argument('--competition-root',type=Path);args=parser.parse_args()
 if args.competition_root:TARGETS['lineops-agentware-2026']=args.competition_root
 if args.project in ('full','both'):
  export('lineops-agent-platform',full(),1,'完整平台将工作台、运行管理、Agent、工具、感知计算、设备适配和产线世界分为七层。控制查询、数据证据与状态变更使用独立路径；右侧展开“干预后再验证”的闭环，底部说明稳定契约与评测真值隔离。', '<p><strong>a 系统分层：</strong>先看职责归属和嵌套边界，再沿不同颜色追踪调用与反馈。</p><p><strong>b 处置闭环：</strong>动作改变世界，新观测才能支持恢复；未恢复则重新规划或移交。</p><p><strong>c 兼容性：</strong>产线、感知任务和计算后端通过共同契约接入，新适配仍需实现与验收。</p><p><strong>d 证据隔离：</strong>隐藏故障用于产生观测和离线评分，不直接提供给 Agent。</p>')
 if args.project in ('competition','both'):
  export('lineops-agentware-2026',competition(),2,'比赛版本围绕一个有预算、有工具动作、有因果反馈的点胶事件展开。上部区分 Agent 控制面与软件产线，下部列出恢复、移交、停止和失败的不同终态，以及评委可以检查的证据。', '<p><strong>a 自主任务：</strong>异常进入后，由确定性运行管理组织三个角色调用受限工具。</p><p><strong>b 因果反馈：</strong>观测由世界状态产生，动作改变世界，而非由模型结论控制画面。</p><p><strong>c 可靠终态：</strong>恢复必须复核；移交必须暂停并建单；预算、人工停止与异常各有出口。</p><p><strong>d 演示证据：</strong>展示新旧图像、实际回执、固定恢复谓词和可回放轨迹。</p>')
