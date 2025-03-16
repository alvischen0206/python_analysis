import pandas as pd
import logging

# 設定 logging 的基本配置
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    主函數，用於處理上市公司資料並進行整理和儲存。
    """
    logging.debug("程式開始執行")

    try:
        # 讀取 CSV 檔案，檔案名為 '上市公司資料.csv'
        logging.debug("嘗試讀取 '上市公司資料.csv' 檔案")
        df = pd.read_csv('上市公司資料.csv')
        logging.debug("成功讀取 '上市公司資料.csv' 檔案")
    except FileNotFoundError:
        logging.error("找不到 '上市公司資料.csv' 檔案，請確認檔案是否存在")
        return
    except Exception as e:
        logging.error(f"讀取 '上市公司資料.csv' 檔案時發生錯誤: {e}")
        return

    # 顯示 DataFrame 的資訊，包括列名、非空值數量和資料類型
    logging.debug("顯示原始 DataFrame 的資訊")
    df.info()

    # 移除 DataFrame 中包含 NaN 值的行，並將結果儲存到 df1
    logging.debug("移除包含 NaN 值的行")
    df1 = df.dropna()
    logging.debug(f"移除 NaN 後，剩餘 {len(df1)} 行")
    # 顯示 df1 的資訊
    logging.debug("顯示移除 NaN 後的 DataFrame 資訊")
    df1.info()

    # 重新索引 DataFrame，只保留指定的列，並將結果儲存到 df2
    logging.debug("重新索引 DataFrame，只保留指定的列")
    df2 = df1.reindex(columns=['公司代號','出表日期','公司名稱','產業別','營業收入-當月營收','營業收入-上月營收'])
    logging.debug(f"重新索引後，DataFrame 的列名為: {df2.columns.tolist()}")

    # 使用 query 方法篩選出 '產業別' 為 '水泥工業' 的行，但結果沒有被儲存
    logging.debug("篩選 '產業別' 為 '水泥工業' 的行 (結果未儲存)")
    cement_industry_df = df2.query('產業別=="水泥工業"')
    logging.debug(f"篩選出 {len(cement_industry_df)} 行 '產業別' 為 '水泥工業' 的資料")

    # 重新命名 df2 中的列名，將 '營業收入-上月營收' 改為 '上月營收'，'營業收入-當月營收' 改為 '當月營收'，並將結果儲存到 df3
    logging.debug("重新命名列名")
    df3 = df2.rename(columns={
        '營業收入-上月營收':'上月營收',
        '營業收入-當月營收':'當月營收'
        })
    logging.debug(f"重新命名後，DataFrame 的列名為: {df3.columns.tolist()}")

    # 將 df3 儲存為 CSV 檔案，檔案名為 '上市公司資料_整理.csv'，使用 utf-8-sig 編碼，不包含索引
    logging.debug("儲存 DataFrame 到 '上市公司資料_整理.csv'")
    try:
        df3.to_csv('上市公司資料_整理.csv', encoding='utf-8-sig', index=False)  # 存檔
        logging.debug("成功儲存 '上市公司資料_整理.csv'")
    except Exception as e:
        logging.error(f"儲存 '上市公司資料_整理.csv' 時發生錯誤: {e}")
        return
    
    # 將 df3 儲存為 Excel 檔案，檔案名為 '上市公司資料_整理.xlsx'，不包含索引
    logging.debug("儲存 DataFrame 到 '上市公司資料_整理.xlsx'")
    try:
        df3.to_excel('上市公司資料_整理.xlsx', index=False)  # 存檔
        logging.debug("成功儲存 '上市公司資料_整理.xlsx'")
    except Exception as e:
        logging.error(f"儲存 '上市公司資料_整理.xlsx' 時發生錯誤: {e}")
        return

    # 印出提示訊息，表示檔案已儲存完成
    print('檔案已存檔完成')
    logging.debug("程式執行完成")

# 判斷是否為主程式執行，如果是則執行 main 函數
if __name__ == '__main__':
    main()
