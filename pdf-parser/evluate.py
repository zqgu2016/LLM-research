import openai


def compare_markdown_versions_without_format(segment1, segment2, segment3, segment4, original_text):
    prompt = f"""
    这是从PDF原文上使用4种PDF解析器提取的，请对照原文基于以下3个指标进行评价。满分5分，根据这几项进行打分，输出markdown表格

    1. **准确识别单词**：是否存在提取的文本错误，忽略错误的单词分隔和连字符等问题。
    3. **保持段落完整性**：嵌入的元素如公式或图像或者图像标题可能会导致段落被打断，或者将标题错误地合并到正文中。如果原文有图像，但是转换的markdown没有图像，则需要扣分。
    3. **保持原文语义**：是否存在多提取的内容，导致文本不对。

    Original Text:
    {original_text}

    ===================
    Markdown Generated by Nougat:
    {segment1}

    ===================
    Markdown Generated by TextIn:
    {segment2}
    
    ===================
    Markdown Generated by PyMuPDF4LLM
    {segment3}
    
    ===================
    Markdown Generated by Another Vendor
    {segment4}
    
    =======
    这是从PDF原文上使用4种PDF解析器提取的，请对照原文基于以下3个指标进行评价。满分5分，根据这几项进行打分，输出markdown表格

    1. **准确识别单词**：是否存在提取的文本错误，忽略错误的单词分隔和连字符等问题。
    2. **保持段落完整性**：嵌入的元素如公式或图像可能会导致段落被打断，或者将标题错误地合并到正文中。如果原文有图像，但是转换的markdown没有图像，则需要扣分。
    3. **保持原文语义**：是否存在多提取的内容，导致文本不对。
    """

    client = openai.OpenAI(
        api_key="xxx.xxxx",
        base_url="https://open.bigmodel.cn/api/paas/v4"
    )

    # 调用GPT模型进行对比
    response = client.chat.completions.create(
        model="glm-4-plus",  # 选择合适的模型
        messages=[
            {"role": "system", "content": "你是一个专业Markdown对比助手"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )

    return response.choices[0].message.content


# 假设你有一个分段后的原文、Markdown版本1、版本2
original_paragraphs = ["""
3.1 DocLayNet Dataset
DocLayNet contains approximately 80,000 document pages. Documents are annotated with 11
distinct elements: Footnote, Formula, List-item,
Page footer, Page-header, Picture, Section header,
Table, Text, and Title. The documents provided
in the DocLayNet dataset are classified into 6
distinct categories: Financial Reports, Manuals,
Scientific Articles, Laws and Regulations, Patents,
and Government Tenders. The distribution of
these categories is provided in Figure 1. These documents are mostly in English (95%), with a few
documents in German (2.5%), French (1%), and
Japanese (1%).
The other datasets[17][18]mainly contain scientific documents taken from repositories such as
arXiv or PubMed. These datasets have limited
variability in layout as they follow more or less

![Law and Regulation Financial 16.0% 32.0% Tenders 6.0% 21.0% 17.0% 8.0% Manuals Scientific Patents ](https://web-api.textin.com/ocr_image/external/b28b34d35eb41fb0.jpg)

Fig. 1 Distribution of document categories in DocLaynet Dataset[13]
uniform templates. However, DocLayNet provides a wide range of document layouts. The ‘Financial’ and ‘Manual’ categories include a large num- ber of freestyle documents. Specifically, Financial Reports consist of both annual reports in freestyle format and formal SEC (Securities and Exchange Commission) filings, while the Manuals category
comprises documents such as instructions for com- puter program manuals and grammar guides. The remaining categories - Scientific Articles, Laws and Regulations, Patents, and Government Ten- ders - contain documents from various websites and publishers, further increasing the variability in document layouts. To ensure the high quality and reliability of the annotations, around 7,059 documents were doubly annotated, and 1,591 doc- uments were triply annotated. This means these documents were independently annotated by two or three different annotators respectively, allowing for the determination of inter-annotator agree- ment.
DocLayNet’s ‘core’ dataset contains JSON files in standard COCO format[30] with images (PNG). Each JSON file has information such as document category, document name, precedence (non-zero in case of redundant double- or triple-annotation), bounding box coordinates, and text inside the bounding boxes. DocLayNet’s ‘extra’ dataset con- tains PDF and JSON files which include the text and bounding box coordinates. Both datasets con- tain files split into test, train, and validation sets.

"""]
markdown_nougat = ["""
### DocLayNet Dataset

DocLayNet contains approximately 80,000 document pages. Documents are annotated with 11 distinct elements: Footnote, Formula, List-item, Page footer, Page-header, Picture, Section header, Table, Text, and Title. The documents provided in the DocLayNet dataset are classified into 6 distinct categories: Financial Reports, Manuals, Scientific Articles, Laws and Regulations, Patents, and Government Tenders. The distribution of these categories is provided in Figure 1. These documents are mostly in English (95%), with a few documents in German (2.5%), French (1%), and Japanese (1%).

The other datasets[17][18]mainly contain scientific documents taken from repositories such as arXiv or PubMed. These datasets have limited variability in layout as they follow more or less uniform templates. However, DocLayNet provides a wide range of document layouts. The 'Financial' and 'Manual' categories include a large number of freestyle documents. Specifically, Financial Reports consist of both annual reports in freestyle format and formal SEC (Securities and Exchange Commission) filings, while the Manuals category

\begin{table}
\begin{tabular}{l l l l l l} \hline \hline
**Dataset** & **Size** & **Source** & **Document Type** & **GTE** & **Annotation** \\ \hline GIANT [23] & 1B & Crossref & Research articles & R & Automatic(XML) \\ S2ORC[24] & 8.1M & Semantic Scholar & Research articles & R, FT & Automatic(Latex) \\ PubLayNet[17] & 360k & PubMed & Biomedical articles & FT & Automatic(XML) \\ SciTSR[25] & 15k & arXiv & Research articles & T & Automatic(Latex) \\ Bast[5] & 12k & arXiv & Scientific articles & FT & Automatic(Text) \\ DocBank[18] & 500k & arXiv & Research articles & FT & Automatic(Text) \\ FinTabNet[26] & 89k & Multiple sources & Annual financial reports & T & Automatic(XML) \\ PubTables-1M[20] & 1M & PubMed & Scientific articles & T & Automatic(XML) \\ DocLayNet[13] & 80k & Multiple sources & Multiple & FT & Manual \\ M6Doc[19] & 9k & Multiple sources & Multiple & FT & Manual \\ SciBank[27] & 74k & arXiv & Scientific articles & FT & Automatic(Latex) \\ \hline \hline \end{tabular}
\end{table}
Table 1: Overview of commonly cited datasets for information extraction from PDFs, detailing various types of ground truth elements (GTE) including references (R), full text with layout details (FT), and tables (T). The ground truth elements were generated either automatically using XML or LaTeX files, or manually with human intervention.

\begin{table}
\begin{tabular}{l c c c c c} \hline \hline
**Paper** & **Dataset Size** & **Document Type** & **Metrics** & **Elements** & **No. of tools** \\ \hline Tkaczyk[8] & 9,491 & Scientific & P, R, F1 & References & 10 \\ Bast[5] & 12,000 & Scientific & Custom & Multiple & 14 \\ Lipinski[28] & 1,253 & Scientific & Accuracy & Metadata & 9 \\ Meuschke[29] & 500,000 & Academic & P, R, F1 & Multiple & 10 \\ \hline \hline \end{tabular}
\end{table}
Table 2: Summary of studies comparing PDF parsers Evaluation metrics used by the studies: Precision(P), Recall(R), and F1 Score.

Figure 1: Distribution of document categories in DocLaynet Dataset[13]

comprises documents such as instructions for computer program manuals and grammar guides. The remaining categories - Scientific Articles, Laws and Regulations, Patents, and Government Tenders - contain documents from various websites and publishers, further increasing the variability in document layouts. To ensure the high quality and reliability of the annotations, around 7,059 documents were doubly annotated, and 1,591 documents were triply annotated. This means these documents were independently annotated by two or three different annotators respectively, allowing for the determination of inter-annotator agreement.

DocLayNet's 'core' dataset contains JSON files in standard COCO format[30] with images (PNG). Each JSON file has information such as document category, document name, precedence (non-zero in case of redundant double- or triple-annotation), bounding box coordinates, and text inside the bounding boxes. DocLayNet's 'extra' dataset contains PDF and JSON files which include the text and bounding box coordinates. Both datasets contain files split into test, train, and validation sets.
"""]
markdown_textin = ["""
#### 3.1 DocLayNet Dataset

DocLayNet contains approximately 80,000 docu-ment pages. Documents are annotated with 11distinct elements: Footnote, Formula, List-item,Page footer,Page-header, Picture,Section header,Table, Text, and Title. The documents provided in the DocLayNet dataset are classified into 6distinct categories: Financial Reports,Manuals,Scientific Articles,Laws and Regulations,Patents,and Government Tenders. The distribution of these categories is provided in Figure 1. These doc-uments are mostly in English (95%), with a few documents in German (2.5%), French(1%),and Japanese(1%).

The other datasets[17][18]mainly contain sci-entific documents taken from repositories such as arXiv or PubMed. These datasets have limited variability in layout as they follow more or less


![Law and Regulation Financial 16.0% 32.0% Tenders 6.0% 21.0% 17.0% 8.0% Manuals Scientific Patents ](https://web-api.textin.com/ocr_image/external/b28b34d35eb41fb0.jpg)

Fig.1 Distribution of document categories in DocLaynet Dataset[13]

uniform templates. However, DocLayNet provides a wide range of document layouts. The 'Financial'and 'Manual' categories include a large num-ber of freestyle documents. Specifically, Financial Reports consist of both annual reports in freestyle format and formal SEC (Securities and Exchange Commission) filings, while the Manuals category

comprises documents such as instructions for com-puter program manuals and grammar guides. The remaining categories - Scientific Articles, Laws and Regulations, Patents, and Government Ten-ders - contain documents from various websites and publishers, further increasing the variability in document layouts. To ensure the high quality and reliability of the annotations, around 7,059documents were doubly annotated, and 1,591 doc-uments were triply annotated. This means these documents were independently annotated by two or three different annotators respectively,allowing for the determination of inter-annotator agree-ment.

DocLayNet's 'core' dataset contains JSON files in standard COCO format[30] with images (PNG).Each JSON file has information such as document category, document name, precedence (non-zero in case of redundant double- or triple-annotation),bounding box coordinates, and text inside the bounding boxes. DocLayNet's 'extra'dataset con-tains PDF and JSON files which include the text and bounding box coordinates. Both datasets con-tain files split into test, train, and validation sets.

"""]
markdown_pymupdf = [
    """
    #### 3.1 DocLayNet Dataset 6.0%


DocLayNet contains approximately 80,000 document pages. Documents are annotated with 11
distinct elements: Footnote, Formula, List-item,
Page footer, Page-header, Picture, Section header,
Table, Text, and Title. The documents provided
in the DocLayNet dataset are classified into 6
distinct categories: Financial Reports, Manuals,
Scientific Articles, Laws and Regulations, Patents,
and Government Tenders. The distribution of
these categories is provided in Figure 1. These documents are mostly in English (95%), with a few
documents in German (2.5%), French (1%), and
Japanese (1%).
The other datasets[17][18]mainly contain scientific documents taken from repositories such as
arXiv or PubMed. These datasets have limited
variability in layout as they follow more or less


Fig. 1 Distribution of document categories in DocLaynet
Dataset[13]

uniform templates. However, DocLayNet provides
a wide range of document layouts. The ‘Financial’
and ‘Manual’ categories include a large number of freestyle documents. Specifically, Financial
Reports consist of both annual reports in freestyle
format and formal SEC (Securities and Exchange
Commission) filings, while the Manuals category


4


-----

comprises documents such as instructions for computer program manuals and grammar guides. The
remaining categories - Scientific Articles, Laws
and Regulations, Patents, and Government Tenders - contain documents from various websites
and publishers, further increasing the variability
in document layouts. To ensure the high quality
and reliability of the annotations, around 7,059
documents were doubly annotated, and 1,591 documents were triply annotated. This means these
documents were independently annotated by two
or three different annotators respectively, allowing
for the determination of inter-annotator agreement.
DocLayNet’s ‘core’ dataset contains JSON files in
standard COCO format[30] with images (PNG).
Each JSON file has information such as document
category, document name, precedence (non-zero in
case of redundant double- or triple-annotation),
bounding box coordinates, and text inside the
bounding boxes. DocLayNet’s ‘extra’ dataset contains PDF and JSON files which include the text
and bounding box coordinates. Both datasets contain files split into test, train, and validation
sets.
    """
]

markdown_ano_vendor = [
    """
    3.1 DocLayNet Dataset
DocLayNet contains approximately 80,000 docu-ment pages. Documents are annotated with 11 distinct elements: Footnote, Formula, List-item, Page footer, Page-header, Picture, Section header, Table, Text, and Title. The documents provided in the DocLayNet dataset are classified into 6 distinct categories: Financial Reports, Manuals, Scientific Articles, Laws and Regulations, Patents, and Government Tenders. The distribution of these categories is provided in Figure 1. These doc-uments are mostly in English (95%), with a few documents in German (2.5%), French (1%), and Japanese (1%).
The other datasets[17][18]mainly contain sci-entific documents taken from repositories such as arXiv or PubMed. These datasets have limited variability in layout as they follow more or lessFig. 1 Distribution of document categories in DocLaynet Dataset[13]

uniform templates. However, DocLayNet provides a wide range of document layouts. The ‘Financial’ and ‘Manual’ categories include a large num-ber of freestyle documents. Specifically, Financial Reports consist of both annual reports in freestyle format and formal SEC (Securities and Exchange Commission) filings, while the Manuals category
comprises documents such as instructions for com-puter program manuals and grammar guides. The remaining categories - Scientific Articles, Laws and Regulations, Patents, and Government Ten-ders - contain documents from various websites and publishers, further increasing the variability in document layouts. To ensure the high quality and reliability of the annotations, around 7,059 documents were doubly annotated, and 1,591 doc-uments were triply annotated. This means these documents were independently annotated by two or three different annotators respectively, allowing for the determination of inter-annotator agree-ment.
DocLayNet’s ‘core’ dataset contains JSON files in standard COCO format[30] with images (PNG). Each JSON file has information such as document category, document name, precedence (non-zero in case of redundant double- or triple-annotation), bounding box coordinates, and text inside the bounding boxes. DocLayNet’s ‘extra’ dataset con-tains PDF and JSON files which include the text and bounding box coordinates. Both datasets con-tain files split into test, train, and validation sets.
    
    """
]

# 对比每个段落
for original, seg1, seg2, seg3, seg4 in zip(original_paragraphs, markdown_nougat, markdown_textin, markdown_pymupdf, markdown_ano_vendor):
    comparison = compare_markdown_versions_without_format(seg1, seg2, seg3, seg4, original)
    print(comparison)
    print("####################################")