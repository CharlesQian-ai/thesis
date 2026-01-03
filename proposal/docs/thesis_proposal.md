---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3044022045608cc14159344f9eafe66ddb206f3dd22fd50c50722cea7f869b3e08f0524802204ad51b2e93e402225e3a60781a4768a5d7c36143bf4f3369f4f27e485a38e7cd
    ReservedCode2: 3044022030ddf722907d485387372f28521c167040fe3ffda093cbbfe57a1584917ab32002204af3584cdb125568ce7179b0b979f3f4274c48210ef48bac16cae8dfa12e7f28
---

基于空间-频域协同与极性感知的

文本引导目标计数研究

# 引言

## 研究背景

目标计数作为计算机视觉领域的基础性研究任务，其核心价值在于从复杂视觉场景中精准估算特定类别物体的数量，这一技术在智慧城市治理、精准农业监测、工业自动化质检、医学病理诊断以及生态资源调查等诸多领域均展现出不可替代的应用潜力。传统目标计数方法往往遵循"专类专用"的研发范式，即针对人群、车辆、细胞等特定类别设计定制化模型。这类方法虽然在封闭域内取得了一定成效，但其本质缺陷在于对训练数据分布的强烈依赖，即当部署环境出现训练阶段未见的物体类别时，模型性能往往呈现断崖式下跌，难以满足开放世界动态场景的应用需求。近年来，随着通用人工智能技术的发展，研究范式正从"封闭集识别"向"开放集理解"深刻转型，类不可知（class-agnostic）的计数方法应运而生，成为学术界与工业界共同关注的焦点。

在类不可知计数的技术演进路径中，先后涌现出少样本学习、无参考学习及零样本学习等多种范式。少样本计数方法如FamNet[1]、CounTR[2]等通过用户提供1-3个视觉样例实现新类别适配，虽降低了数据依赖，但仍无法摆脱人工干预的桎梏。无参考计数方法如RCC[3]、LOCA[4]尝试完全摆脱样例约束，却丧失了指定目标类别的能力，难以应对"计数图像中所有螺丝钉"这类精细化需求。文本引导的零样本计数（Text-guided Zero-shot Object Counting, TZOC）由Xu[5]等人在CVPR 2023首次系统提出，该范式革命性地引入自然语言描述作为语义指引，用户仅需输入"car"或"apple"等文本提示，模型即可在无需任何视觉样例的情况下完成计数任务，极大提升了系统的自主性与交互友好性。然而，现有TZOC方法在跨模态对齐的本质问题上仍存在显著不足：CLIP-Count[6]等方法采用简单的余弦相似度计算，将复杂的跨模态交互简化为向量点积，无法捕捉"带把手的杯子"这类细粒度语义关联；同时，绝大多数研究过度依赖视觉编码器的顶层特征，忽略了中间层蕴含的层次化纹理、形状及部件信息，导致在小目标、遮挡目标等挑战性场景下定位精度受限。此外，现有方法几乎完全聚焦于空间域特征建模，对频率域携带的结构周期性、边缘强度等关键信息利用不足，而这些信息对于区分"透明瓶身"与"金属瓶盖"等相似目标至关重要。

本研究针对当前技术瓶颈，系统探索空间-频率域多视角特征融合机制与极性感知的跨模态注意力机制，旨在在零样本目标计数的基础理论与工程实践层面实现双重突破。研究将深入挖掘Transformer中间层特征的互补潜力，创新性地引入无偏快速傅里叶卷积[7]技术以解构频率，设计正负子空间分离的极性注意力机制，显式强化目标与背景的判别性特征，并有效抑制矛盾信息，最终构建一个兼具高精度与强泛化能力的零样本目标计数框架。

## 研究意义

理论意义：本研究拟提出自适应多视角特征融合与金字塔极性感知交叉注意力机制，将多模态融合从单一空间域拓展至空间-频率域协同，从全局向量匹配深化至正负子空间分解，为跨模态对齐理论提供新的技术路径。研究将深入探索频率域特征在高层语义任务中的表征机理，阐明其对目标结构信息的捕获逻辑，丰富计算机视觉中频谱分析的应用理论体系。极性感知注意力的提出将传统注意力机制中的"相关性计算"升级为"判别性证据强化"，为提升模型在开放世界中的鲁棒决策能力提供可解释性更强的理论依据。

实践意义：研究成果可直接应用于无人机巡检、零售货架管理、生态监测等场景，实现即插即用式的开放类别计数，降低AI落地门槛。预期在跨数据集评估中验证的域泛化能力，可为实际部署中面临的视觉环境偏移问题提供有效解决方案，具有重要的工程应用价值。

# 国内外研究现状及分析

## 国内外研究现状

在早期，对于目标计数模型的研究主要集中于特定领域的特定类型目标的计数。然而，在2021年，美国石溪大学团队提出了使用少样本策略进行类不可知计数的网络结构，并公开了可知目标计数基准数据集FSC-147[1]。这一工作推动了目标计数模型研究朝着更具普适性的类不可知计数方向发展。类不可知计数是指在没有预定义类别信息的情况下，对未知类别的目标进行计数。这种情况下，模型需要具备辨别和计数未见过的目标的能力。

### 特定类型的目标计数

特定类别目标计数是指针对特定类别的对象进行计数的任务，例如人群计数、车辆计数、农作物计数和细胞计数等。在各个领域中，针对特定类别目标计数的研究都取得了许多显著的研究成果。

在人群计数领域，Zhang等提出了一种多列卷积神经网络（Multi-column Convolutional Neural Network, MCNN） [9]结构来将图像映射到其人群密度图中，并引入了人群计数领域的基准数据集：ShanghaiTech人群数据集。Liang等提出的CrowdCLIP[10]利用多模态排序损失，在训练过程中通过构建排序文本提示来匹配大小排序的群体斑块，以指导图像编码器的学习，在测试过程中渐进滤波策略处理图像斑块的多样性。

在车辆计数领域，Hsieh等提出布局建议网络（Layout Proposal Networks, LPNs）[11]和空间内核，以同时统计和定位由无人机录制的视频中的目标物体，同时他们引入了一个新的大型汽车停车场数据集：CARPK，该数据集成为了车辆计数领域的基准数据集。Kilic等提出了热力图学习器卷积神经网络（Heatmap Learner Convolutional Neural Network, HLCNN）[12]，该网络改进了CNN的结构，增加了三个卷积层作为适配层来学习目标汽车的热力图。

在农作物计数领域，鲍等人[13]提出了一种适用于自然场景中的小麦图像计数方法。该方法通过多尺度及多方向分解技术对小麦穗特征进行增强，同时有效降低背景噪声。继而，运用阈值分割技术对小麦穗图像进行切割，再应用形态学处理技术分离出含小麦穗信息的区域。最后，采用最大值查找方法计算小麦穗数量。Lu等人提出了一种名为TasselNet[8]的局部计数回归网络，通过对局部图像进行计数。通过合并和归一化所有结果，可以获得相应的计数映射。尽管TasselNet在处理玉米穗的计数方面取得了一定成果，但当将其应用于小麦穗的计数时，却无法预测准确的结果。因此，在之后的研究中，Xiong等人提出了TasselNetv2[14]，在卷积神经网络的局部块中添加了上下文信息，以改善小麦穗计数的准确性。

在细胞计数领域，Xue等[15]提出了一种基于CNN的监督学习框架，将细胞计数问题转化为回归问题，使用全局细胞数量作为监督信号，训练网络以回归出正确的细胞数量。Aldughayfiq等[16]采用YOLOv5[17]和特征金字塔（Feature Pyramid Network, FPN）[18]来计数荧光显微图像中的多种尺度的细胞。

### 少样本目标计数

少样本目标计数算法的目的是学习一个广义模型，该模型在推理阶段可以利用标注框作为示例样本，从而推断任意感兴趣的目标的数量。通过使用Few-shot学习方法，模型可以在只有少量样本的情况下学习新类别的特征，并进行计数任务。这种方法的提出使得目标计数模型具备了更广泛的适用性和泛化能力。

作为类不可知计数领域一项开创性的工作，Lu等提出了一种通用匹配网络（General Matching Network, GMN）[19]，该方法通过一个共享权重的卷积神经网络来提取查询集和支持集的特征映射，并将这些特征拼接起来以进行回归计数。

随后，Ranjan等提出了小样本适应和匹配网络（Few-shot adaptation & matching Network, FamNet）[1]。FamNet使用ROI Pooling的方法，仅针对感兴趣的区域提取特征，并在测试阶段设计了一种新颖的小样本自适应方案，以实现对未知新类别目标的计数泛化。此外，他们引入了一个名为FSC-147的基准数据集，该数据集是第一个在类不可知目标计数方面挑战覆盖遮挡和尺度变化等问题的大规模数据集。

后续的研究主要分为两个分支。一个是基于特征的方法，这种方法利用更强大的视觉主干网络，来提取更好的特征表示，例如CounTR[2]使用vision transformer(ViT)[20]作为视觉编码器；LOCA[4]提出了新的对象原型提取模块，它迭代地将范例的形状和外观信息与图像特征融合。另一个分支是基于相似度的方法，这种方法通过明确地建模示例图像与查询图像之间的相似性来优化匹配过程，例如BMNet[21]提出了一种相似性感知的类不可知计数（Class Agnostic Counting, CAC）框架，该框架能够同时学习特征表示和相似度度量；SAFECount[22]提出了一个用于目标计数的相似感知特征增强模块，通过更多地关注与支持图像类似的区域来检测查询图像，从而使不同目标对象之间的边界更加清晰。

尽管这些方法在性能上表现良好，但在训练和推断阶段都需要额外的图像块标注，这可能会产生较高的成本。

### 无参照目标计数

无参照物目标计数算法的目的是在没有任何参考样本的情况下，对可能感兴趣的目标进行计数。它不依赖于任何预定义的参考样本，而是通过分析图像中的特征和结构来估计目标的数量。

Ranjan等在继少样本计数网络FamNet[1]之后提出了重复区域建议网络（Repetitive Region Proposal Network, RepRPN）[23]。RepRPN是一种无参照样本的计数网络，它提出了一种新的区域建议网络来识别范例，在识别出样本后，使用基于密度估计的视觉计数器得到相应的计数。

Hobley等提出了一种弱监督的无参照类不可知计数网络（Reference-less Class-agnostic Counting, RCC）[3]。RCC利用预训练的ViT[20]来隐式提取可能感兴趣的对象，并直接回归一个标量作为估计的目标计数。

虽然这些方法不需要示例样本，但在存在多个目标类别的情况下，它们未能提供一种指定感兴趣目标的方式。

### 零样本目标计数

零样本文本引导计数作为当前最前沿范式，其核心挑战在于文本语义如何稳定地对齐到图像中的“实例级区域”，并在开放类别、复杂背景与密集小目标场景下保持可泛化的定位与计数能力。Xu等提出了一个新的计数方法[5]，在推理时只需要提供类名来定义要计数的内容，而不是范例。他们采用了一个两阶段的训练方案。CLIP-Count[6]开创性地引入CLIP视觉/文本编码器，并在计数数据上以对比学习方式训练轻量适配器，使“图—文”在共享语义空间中更可分；但其对齐通常依赖最终层全局表征或单层相似度点积，空间细节与实例边界信息容易被稀释，导致细粒度对应与密集目标定位不足。VLCounter[24]进一步将CLIP的语义与patch间的关联用于端到端计数：一方面通过语义条件的提示/调优让视觉特征更“目标突出”，另一方面对语义—patch相似度图做可学习的映射/校准以适配计数需求，并利用编码器中间层特征的层间传递补充多尺度线索，从而缓解只看最后一层带来的信息损失，但其核心仍以相似度图为主线，细粒度判别往往受限于相似度建模形式。VA-Count[25]则更强调“可用exemplar的质量与噪声抑制”对零样本计数的决定性作用：通过检测/grounding类模块生成候选patch并进行exemplar增强，再结合密度线索或对比目标区分机制抑制误检噪声，提高exemplar可靠性；不过两阶段候选生成与筛选仍可能在极密集或尺度极端变化时出现漏检/误检累积。ExpressCount[26]提出语言驱动的“虚拟样例”思路：由文本预测样例特征并与视觉特征进行交叉注意力交互，从而在无需人工框样例的情况下提供“计数参照”，但虚拟样例一旦偏离真实外观分布，误导效应会直接传导到计数结果，稳定性受限。上述方法普遍存在三个共性局限：其一，交互尺度偏单一，虽开始引入中间层信息，但对层次化/多尺度结构的系统融合仍不足；；其二，相似度机制偏静态，缺少面向“目标—背景可分性”的自适应强化与难例抑制；其三，结构先验利用不足，尤其对纹理相近类别与复杂背景干扰，缺少频率域或更强形状结构约束来提升可分性与鲁棒性。

### 视觉-语言模型

视觉基础模型与相关技术的发展为本研究提供基石。CLIP[27]采用双塔结构，在4亿图文对上通过对比学习训练，其损失函数设计为对称交叉熵，确保图像与文本嵌入在共享空间对齐。但CLIP最后一层[CLS]token聚合全局信息，空间细节丢失。DINOv2[28]通过自蒸馏与中心裁剪策略，输出具备明确语义的patch级特征，在特征图上可直接观察到物体轮廓。

**参考文献**

[1]	RANJAN V, SHARMA U, NGUYEN T, 等. Learning To Count Everything[C/OL]//2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 2021: 3393-3402. DOI:10.1109/CVPR46437.2021.00340.

[2]	LIU C, ZHONG Y, ZISSERMAN A, 等. CounTR: Transformer-based Generalised Visual Counting[C/OL]//33rd British Machine Vision Conference 2022, BMVC 2022, London, UK, November 21-24, 2022. BMVA Press, 2022. https://bmvc2022.mpi-inf.mpg.de/0370.pdf.

[3]	HOBLEY M, PRISACARIU V. Learning to Count Anything: Reference-less Class-agnostic Counting with Weak Supervision[J]. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2023.

[4]	DUKIC N, LUKEZIC A, ZAVRTANIK V, 等. A Low-Shot Object Counting Network With Iterative Prototype Adaptation[C/OL]//2023 IEEE/CVF International Conference on Computer Vision (ICCV). 2023: 18826-18835. DOI:10.1109/ICCV51070.2023.01730.

[5]	XU J, LE H, NGUYEN V, 等. Zero-shot object counting[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2023: 15548-15557.

[6]	JIANG R, LIU L, CHEN C. Clip-count: Towards text-guided zero-shot object counting[Z]//Proceedings of the 31st ACM International Conference on Multimedia. 2023: 4535-4545.

[7]	CHU T, CHEN J, SUN J, 等. Rethinking Fast Fourier Convolution in Image Inpainting[C/OL]//2023 IEEE/CVF International Conference on Computer Vision (ICCV). 2023: 23138-23148. DOI:10.1109/ICCV51070.2023.02120.

[8]	LU H, CAO Z, XIAO Y, 等. TasselNet: counting maize tassels in the wild via local counts regression network[Z]//Plant methods: 卷 13. 2017: 1-17.

[9]	ZHANG Y, ZHOU D, CHEN S, 等. Single-Image Crowd Counting via Multi-Column Convolutional Neural Network[C/OL]//2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2016: 589-597. DOI:10.1109/CVPR.2016.70.

[10]	LIANG D, XIE J, ZOU Z, 等. CrowdCLIP: Unsupervised Crowd Counting via Vision-Language Model[C/OL]//2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 2023: 2893-2903. DOI:10.1109/CVPR52729.2023.00283.

[11]	HSIEH M R, LIN Y L, HSU W H. Drone-Based Object Counting by Spatially Regularized Regional Proposal Network[C/OL]//2017 IEEE International Conference on Computer Vision. 2017: 4165-4173. DOI:10.1109/ICCV.2017.446.

[12]	KILIC E, OZTURK S. An accurate car counting in aerial images based on convolutional neural networks[Z]//Journal of Ambient Intelligence and Humanized Computing. 2023: 1-10.

[13]	BAO W, ZHANG T, HU G, 等. Wheat Spike Counting in Natural Scenes Based on Multiscale and Multiorientation Decomposition[Z]//Journal of Anhui University (Natural Sciences Edition). 2020.

[14]	XIONG H, CAO Z, LU H, 等. TasselNetv2: in-field counting of wheat spikes with context-augmented local regression networks[Z]//Plant methods: 卷 15. 2019: 150.

[15]	XUE Y, RAY N, HUGH J, 等. Cell Counting by Regression Using Convolutional Neural Network[C]//HUA G, JÉGOU H. Computer Vision – ECCV 2016 Workshops. Cham: Springer International Publishing, 2016: 274-290.

[16]	ALDUGHAYFIQ B, ASHFAQ F, JHANJHI N, 等. YOLOv5-FPN: a robust framework for multi-sized cell counting in fluorescence images[Z]//Diagnostics: 卷 13. 2023: 2280.

[17]	KHANAM R, HUSSAIN M. What is YOLOv5: A deep look into the internal features of the popular object detector[A/OL]. arXiv, 2024[2026-01-03]. http://arxiv.org/abs/2407.20892. DOI:10.48550/arXiv.2407.20892.

[18]	LIN T Y, DOLLAR P, GIRSHICK R, 等. Feature Pyramid Networks for Object Detection[C/OL]//2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). Honolulu, HI: IEEE, 2017: 936-944[2026-01-03]. http://ieeexplore.ieee.org/document/8099589/. DOI:10.1109/CVPR.2017.106.

[19]	LU E, XIE W, ZISSERMAN A. Class-Agnostic Counting[C]//JAWAHAR C V, LI H, MORI G, 等. Computer Vision – ACCV 2018. Cham: Springer International Publishing, 2019: 669-684.

[20]	DOSOVITSKIY A, BEYER L, KOLESNIKOV A, 等. An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale[J]. ICLR, 2021.

[21]	SHI M, LU H, FENG C, 等. Represent, compare, and learn: A similarity-aware framework for class-agnostic counting[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2022: 9529-9538.

[22]	YOU Z, YANG K, LUO W, 等. Few-shot Object Counting with Similarity-Aware Feature Enhancement[C/OL]//2023 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV). Waikoloa, HI, USA: IEEE, 2023: 6304-6313[2026-01-03]. https://ieeexplore.ieee.org/document/10031021/. DOI:10.1109/WACV56688.2023.00625.

[23]	RANJAN V, NGUYEN M H. Exemplar free class agnostic counting[C]//Proceedings of the Asian Conference on Computer Vision. 2022: 3121-3137.

[24]	KANG S, MOON W, KIM E, 等. VLCounter: Text-Aware Visual Representation for Zero-Shot Object Counting[C]//Proceedings of the AAAI Conference on Artificial Intelligence: 卷 38. 2024: 2714-2722.

[25]	ZHU H, YUAN J, YANG Z, 等. Zero-shot Object Counting with Good Exemplars[Z]//arXiv preprint arXiv:2407.04948. 2024.

[26]	WANG M, YUAN S, LI Z, 等. Language-Guided Zero-Shot Object Counting[C/OL]//2024 IEEE International Conference on Multimedia and Expo Workshops (ICMEW). Niagara Falls, ON, Canada: IEEE, 2024: 1-6[2026-01-01]. https://ieeexplore.ieee.org/document/10645452/. DOI:10.1109/ICMEW63481.2024.10645452.

[27]	RADFORD A, KIM J W, HALLACY C, 等. Learning Transferable Visual Models From Natural Language Supervision[C/OL]//International Conference on Machine Learning. 2021. https://api.semanticscholar.org/CorpusID:231591445.

[28]	OQUAB M, DARCET T, MOUTAKANNI T, 等. DINOv2: Learning Robust Visual Features without Supervision[Z/OL]//ArXiv: abs/2304.07193. (2023). https://api.semanticscholar.org/CorpusID:258170077.

## 现有研究存在问题及本文改进的思路

### 存在的主要问题

跨模态交互粗粒度：现有方法依赖单层静态点积相似度计算，将复杂的图文关联简化为标量匹配，无法建模"红色圆形纽扣"这类属性-部件组合语义。正负相关线索在单一内积中混杂，导致目标区域激活不突出，背景干扰难以抑制。

多尺度信息利用不足：绝大多数方法仅使用视觉编码器的顶层输出，忽视第3-9层中间特征蕴含的从边缘、纹理到部件的渐进信息。这种单层依赖使模型对目标尺度变化敏感，难以同时准确计数大物体与小实例。

频率域结构信息缺失：现有方法局限于RGB空间域，对频谱中携带的周期性重复模式、边缘锐度、纹理方向等结构先验利用为零。当目标与背景颜色相近但纹理差异显著时（如透明杯中的水与玻璃杯壁），纯空间特征判别力崩溃。

域泛化能力弱：开放域FSC-147与特定域CARPK的频谱分布存在显著差异，无偏傅里叶卷积在开放域学习到的频率分解策略在特定域失效。跨模态对齐在分布偏移下稳定性不足，导致跨数据集性能衰减严重。

### 改进思路

针对上述问题，本研究基于已探索的两项工作，提出两个独立且互补的解决方案，分别从不同角度攻克零样本计数难题。

方案一（AMS-Counter）：聚焦空间-频率域多视角融合。通过自适应多视角特征融合模块（AMFFM）垂直整合视觉Transformer的第3、6、9层中间特征，构建空间域多视角相似度体积。引入无偏快速傅里叶卷积（UFFC）将该体积变换至频率域，分离高低频分量后逆变换重构，实现"细节-语义-结构"的协同增强。自适应跳过连接（ASC）通过可学习参数动态平衡单视图与多视图贡献，突破传统静态余弦相似度局限。

方案二（PolaCount）：聚焦跨模态判别性增强。设计金字塔极性感知交叉注意力模块（PPCAM），将查询-键向量在通道维度分解为正负独立子空间。正子空间通过可学习非线性函数强化同号共激活，负子空间捕获反号抑制线索，最终相似度为多重交互的代数和，实现"正相关加分、负相关减分"的显式证据强化，使目标语义响应锐化、背景矛盾信息主动抑制。结合多分辨率金字塔结构，逐层传播极性线索，实现尺度自适应的精准对齐。

# 学位论文的研究内容、实施方案及其可行性论证

## 主要研究内容

### 方案一：基于空间-频率域多视角融合的AMS-Counter方法

本方案旨在突破单尺度空间特征局限，构建自适应多视角特征融合体系。

第一，空间域多视角特征提取与相似度计算。研究视觉Transformer第3、6、9层中间特征的互补特性，每层特征独立与文本嵌入计算余弦相似度，生成多层级相似度图[S₁, S₂, S₃]。浅层S₁保留高分辨率细节，适合小目标定位；中层S₂捕获纹理与部件模式，适合区分相似物体；深层S₃编码全局语义，提供类别概念。通过堆叠这些相似度图构建空间域特征体积V_space ∈ ℝ^(H×W×L)，其中L为层数。

第二，频率域结构信息提取与融合。创新性地引入无偏快速傅里叶卷积（UFFC）对V_space进行频率域变换。UFFC通过Range Transform将输入映射至对数频谱空间，缓解FFT的幅度不平衡问题，结合Adaptive Clipping动态裁剪异常激活值，稳定训练过程。变换后的频谱特征V_freq ∈ ℝ^(H×W×L)可显式分离高低频分量：高频分量对应边缘、角点等突变结构，低频分量反映物体整体布局与重复模式。通过可学习的频率门控机制，模型自适应选择对计数任务敏感的频带，增强结构信息表征。

第三，自适应跳过连接融合机制。设计自适应跳过连接（ASC）模块，将原始单视图相似度图S_orig与频率增强后的多视图体积V'_space融合。ASC采用双分支结构：主分支通过1×1卷积压缩V'_space，辅分支保留S_orig的高分辨率细节。可学习权重α ∈ [0,1]动态调控两分支贡献，当输入类别在训练集中常见时，α增大以信任多视图信息；面对完全陌生类别时，α减小以避免引入噪声。最终融合相似度图，实现自适应信息聚合。

### 方案二：基于金字塔极性感知注意力的PolaCount方法

本方案旨在解决跨模态交互判别性不足问题，构建极性敏感的文本-视觉对齐机制。

极性感知相似度计算。设计通道级极性分解策略，将查询向量q和键向量k分别分解为正子空间q⁺、k⁺与负子空间q⁻、k⁻。正子空间通过ReLU函数提取所有正值分量，负子空间取绝对值化后的负值分量。引入可学习非线性函数g(x) = x^e，其中指数e = 1 + α·sigmoid(w)为通道级可训练参数，动态调整各通道响应锐度。极性感知相似度定义为：

该设计实现积极证据强化（同号相乘）与矛盾线索抑制（异号相乘），显著提升目标-背景判别边界。

第二，双向交叉注意力机制。构建文本→视觉与视觉→文本的双向交叉注意力结构。文本→视觉注意力以视觉特征为查询、文本特征为键值，确保"文本描述的物体被关注"；视觉→文本注意力以文本特征为查询、视觉特征为键值，验证"关注区域符合文本语义"。两路输出通过门控融合单元加权合并，门控权重由可学习向量G经sigmoid函数生成，实现自适应双向校验，降低单一方向的误检率。

第三，金字塔多尺度级联结构。设计从1/8到1/2分辨率的四级金字塔结构，每级包含双向交叉注意力块与上采样操作。低分辨率层级捕获目标全局分布，高分辨率层级精炼位置细节。级联过程中，每级输出的极性增强特征通过跳连传递至下一级，形成粗到细的极性线索传播机制。该结构对尺度变化大、密集遮挡场景尤为有效，通过多分辨率信息互补提升计数精度。

## 实施方案及其可行性论证

### 实施方案

本研究采用两个独立并行的技术路线，分别实现两种方案并进行对比分析。

AMS-Counter技术路线：采用DINOv2-Small作为视觉骨干，固定参数并注入可学习提示（每层40个token）。文本编码器采用CLIP-ViT-B/16，通过单层MLP适配器对齐至512维共享空间。视觉特征经AMFFM处理后生成多视角相似度图，输入U-shaped Cross-attention Decoder。解码器采用4级上采样结构，每层包含交叉注意力块、卷积层与跳连，最终回归密度图。

PolaCount技术路线：采用DINOv2-Base作为视觉骨干，保留其patch级特征。文本编码器采用CLIP文本分支，通过适配器对齐。核心PPCAM模块由4级双向极性感知注意力块级联构成，每级包含文本→视觉与视觉→文本两个子块。金字塔输出经轻量级CNN解码器上采样至原始分辨率，生成密度图。

### 可行性论证

在理论可行性方面，多视角学习与频率域分析已在图像分割、目标检测等任务中被反复验证能够提升特征表达的判别性与鲁棒性，将其迁移到目标计数任务具有充分的合理性与可解释性；同时，极性分解通过正负响应分离与增强来突出关键判别线索，已在单模态视觉任务中取得良好效果，将该思想进一步扩展到跨模态交互场景时，能够对应“目标相关—目标无关”两类语义通道的建模需求，理论路径清晰且易于形成闭环论证。

在技术可行性方面，两项方案所依赖的核心模块已在前期工作中完成初步验证，整体代码框架基于 PyTorch 搭建，网络组件与训练流程的接口设计清晰，便于后续按模块逐步替换、插拔与扩展，同时也利于开展消融实验与对比实验以定位增益来源。

在资源可行性方面，实验室 GPU 服务器能够支持多组并行训练与参数搜索，公开数据集（如 FSC-147 等）获取便捷且已形成标准评测协议，可直接用于训练与评估；同时现有计算资源能够覆盖多视角特征融合、频率域分支以及跨模态交互模块带来的额外开销，从而保证实验推进的可持续性与结果复现的稳定性。

## 年度研究计划及预期研究结果

本研究以一年为周期，围绕“空间—频率域多视角融合（AMS-Counter）”与“金字塔极性感知跨模态注意力（PolaCount）”两条路线并行推进，按“基线复现—方法实现—系统验证—论文固化”的节奏组织工作，确保每阶段均形成可验收产出。

在1—2月，完成FSC-147、CARPK等数据集处理与评测协议统一，复现并对齐CLIP-Count、VLCounter、ExpressCount等代表性基线，固化训练/推理脚本与指标统计模板，形成可靠对照组。3—5月，集中完成AMS-Counter的模块集成与消融验证，重点评估多层特征融合与空间—频率域增强对密集目标与复杂背景场景的改进效果，得到稳定可训练版本与关键可视化证据。6—8月，完成PolaCount的极性分解与金字塔级联实现，开展与点积/仿射相似度等机制的对照实验，验证其在目标—背景可分性与细粒度语义提示下的增益来源。9—10月，统一两条路线的实验设置，完成跨数据集/跨场景对比、失败案例分析与复杂度评估，形成完整实验结论链。11—12月，完成论文撰写与成果凝练，整理图表、消融矩阵与可解释性结果，按规范完成定稿与答辩准备。

预期研究结果方面，本研究拟形成两套面向零样本文本引导计数的核心算法成果，分别对应空间—频率域多视角融合路线与极性感知判别性交互路线，并在公开基准上完成系统验证与对比分析。其一，形成AMS-Counter算法：通过多层级相似度体积构建与空间—频率域协同增强，实现对密集小目标、尺度变化与复杂背景条件下的更稳健定位与计数，并给出完整的模块消融与可解释性可视化证据链。其二，形成PolaCount算法：通过金字塔极性感知的双向交叉注意力，将跨模态对齐从静态相似度提升为“正相关强化、负相关抑制”的判别性证据聚合，增强目标—背景可分性与细粒度语义提示下的计数稳定性，同样提供充分的对照实验、消融分析与可视化结果支撑上述结论。

# 预期取得的研究成果及创新点情况

## 4.1预期取得的研究成果

### 构建基于空间-频率域多视角融合的零样本目标计数框架（AMS-Counter）

该框架能够同时利用视觉Transformer的多层级空间特征与频率域结构信息，在无需任何视觉样例的条件下，仅通过文本描述即可实现对开放类别目标的精准计数。通过自适应多视角特征融合模块（AMFFM），模型可动态整合不同深度特征，并结合无偏快速傅里叶卷积（UFFC）提取频谱中的周期性模式与边缘结构信息，显著提升在目标密集排列、尺度变化剧烈等复杂场景下的计数准确性。

### 构建基于极性感知跨模态交互的零样本目标计数方法（PolaCount）

该方法能够突破传统注意力机制的局限性，实现文本与视觉特征间判别性的双向交互。通过金字塔极性感知交叉注意力模块（PPCAM），模型将查询-键向量在通道维度分解为正负独立子空间，分别计算同号共激活与异号抑制关系，并代数组合生成锐化的相似度响应。这种设计有效强化与文本描述一致的视觉证据，主动抑制矛盾信息，显著提升目标-背景区分能力，在细粒度语义理解场景下具有更强的鲁棒性。

### 实现面向真实场景部署的域泛化增强机制

该机制能够缓解训练域与测试域数据分布不一致导致的性能衰减问题，提升模型在无人机巡检、人群监控等特定应用场景下的迁移能力。通过视觉提示微调（VPT）策略冻结预训练骨干网络参数，仅训练少量可学习提示token，保留通用视觉表征并降低过拟合风险。结合两阶段渐进式训练策略，先进行跨模态对齐预热，再专注计数任务优化，使模型在不接触目标域数据的情况下，仍能保持较高的计数精度与稳定性。

## 4.2学位论文预期的特色与创新点

本研究基于两个独立且互补的方案分别展开，形成"多视角融合增强"与"判别性交互相位"的双路线技术体系，全面覆盖零样本计数中的特征表示与跨模态对齐核心问题。实验设计不仅包含标准基准评测，更涵盖跨域迁移、消融分析、可视化解释等多维度评估，结论扎实可靠。两项方案均具备理论深度与工程实用性，为开放世界目标计数提供了可复用、可扩展的研究范式。

（1）针对跨模态对齐粒度粗、特征单一的问题，提出空间-频率域多视角融合增强机制。该研究的创新之处在于针对现有零样本计数方法仅依赖顶层空间特征、相似度计算静态单一的问题，提出在频率域与多层级空间域协同工作的特征增强框架。通过AMFFM模块整合不同深度特征的互补信息，并引入UFFC提取频谱结构先验，使模型能够自适应地学习目标周期性分布与边缘结构模式。该框架不仅提高了计数准确性，还增强了对小目标、密集目标的识别能力，降低了对大量训练数据的依赖，具有更好的开放世界泛化能力。

（2）针对跨模态交互判别性弱、目标背景混淆的问题，提出极性感知双向交叉注意力机制。该研究的创新之处在于针对现有注意力机制混合正负相关、缺乏显式判别能力的问题，提出将查询-键向量解耦为正负子空间分别处理的策略。通过PPCAM模块在正负双分支中独立计算相关性与反相关性，并代数组合生成锐化响应，实现积极证据的强化与矛盾线索的抑制。双向交互设计确保文本语义与视觉区域的相互校验，显著提升目标定位的准确性。该方法在处理细粒度描述与复杂背景干扰时表现出更强的鲁棒性。

（3）针对域泛化能力不足、特定场景性能衰减的问题，提出轻量化适配与渐进式训练策略。该研究的创新之处在于针对零样本模型在无人机视角、人群监控等特定域上性能骤降的问题，提出在不破坏预训练通用表征的前提下实现任务适配。通过VPT策略仅微调极少量提示参数，结合跨模态对齐预热与计数任务精调的两阶段训练，有效缓解域偏移带来的性能损失。该策略在保持模型高效性的同时，显著提升了跨数据集迁移的稳定性与可靠性，使其更具备实际部署价值。

# 研究基础与工作条件

## 5.1前期研究进展及相关研究基础

目前已完成了两篇关于零样本目标计数的研究论文。其中，AMS-Counter论文详细介绍了基于空间-频率域多视角融合的零样本计数方法、实验设计、数据集处理以及所获得的实验结果和分析，该方法通过自适应多视角特征融合模块结合无偏快速傅里叶卷积，有效提升了开放类别目标的计数精度，该论文已发表在CCF-B会议ICME 2025。PolaCount论文系统阐述了金字塔极性感知跨模态注意力机制，将查询-键向量解耦为正负子空间分别处理，实现判别性的双向交互，显著增强了目标-背景区分能力，该论文已发表在JCR-Q1期刊Neurocomputing。这两篇论文为本研究的理论框架与技术实现奠定了坚实基础，验证了核心模块的有效性与创新性。

## 5.2已具备的工作条件

硬件方面，实验室已有高性能GPU服务器，满足模型训练需求。软件方面，深度学习框架与相关工具包已配置完毕。数据方面，FSC-147等公开数据集已整理完备。

## 5.3尚缺少的工作条件和拟解决的途径

无。
