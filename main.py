import sys
import os

def validate_arguments(args):
    """验证命令行参数是否有效"""
    if len(args) != 4:
        return False, "参数数量错误！正确格式：python main.py 原文文件路径 抄袭文件路径 结果报告路径"
    
    for path in args[1:3]:
        if not os.path.exists(path):
            return False, f"目标文件不存在：{path}（请检查路径是否正确）"
    
    output_path = args[3]
    if os.path.exists(output_path):
        print(f"警告：结果文件 {output_path} 已存在，运行后将覆盖原有内容！")
    
    return True, "参数验证通过"

def extract_file_info(file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    return file_name, file_size

def load_document(file_path):
    encodings = ['utf-8', 'gbk', 'utf-16', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                return file.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return ""
    
    return ""

def compute_lcs_length(str1, str2):

    m, n = len(str1), len(str2)
    if m == 0 or n == 0:
        return 0
    
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

def calculate_similarity(lcs_len, base_str_len):
    if base_str_len == 0:
        return 0.0
    return (lcs_len / base_str_len) * 100

def generate_report(orig_info, plag_info, similarity):
   
    orig_name, orig_size = orig_info
    plag_name, plag_size = plag_info
    
    report_lines = [
        f"【原文文件】",
        f"  文件名：{orig_name}",
        f"  文件大小：{orig_size} 字节（约 {orig_size//1024:.1f}KB）",
        "",
        f"【抄袭文件】",
        f"  文件名：{plag_name}",
        f"  文件大小：{plag_size} 字节（约 {plag_size//1024:.1f}KB）",
        "",
        f"【查重结果】",
        f"  抄袭文件相似度：{similarity:.2f}%"
    ]
    return "\n".join(report_lines)

def save_report(report_content, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(report_content)
        return True, f"报告已保存至：{os.path.abspath(output_path)}"
    except Exception as e:
        return False, f"报告保存失败：{str(e)}（请检查输出路径权限）"

def main():
    valid, msg = validate_arguments(sys.argv)
    if not valid:
        print(f"参数错误：{msg}")
        sys.exit(1)
    
    orig_path, plag_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]

    orig_info = extract_file_info(orig_path)
    plag_info = extract_file_info(plag_path)

    orig_content = load_document(orig_path)
    plag_content = load_document(plag_path)
    
    if not orig_content:
        print(f"原文文件 {orig_info[0]} 读取失败")
        sys.exit(1)
    if not plag_content:
        print(f"抄袭文件 {plag_info[0]} 读取失败")
        sys.exit(1)

    lcs_len = compute_lcs_length(orig_content, plag_content)
    similarity = calculate_similarity(lcs_len, len(plag_content))

    report = generate_report(orig_info, plag_info, similarity)
    save_success, save_msg = save_report(report, output_path)
    
    if save_success:
        print(save_msg)
    else:
        print(save_msg)
        print("报告内容如下：")
        print("-" * 50)
        print(report)
        print("-" * 50)

    print("论文查重任务完成")

if __name__ == "__main__":
    main()
