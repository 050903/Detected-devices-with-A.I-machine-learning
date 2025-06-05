import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
from .config import DATA_PATH, MODEL_PATH

def train_identifier_model():
    """Tải dữ liệu, huấn luyện mô hình nhận dạng thiết bị và lưu lại."""
    print("Bắt đầu quá trình huấn luyện mô hình nhận dạng...")
    
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file dữ liệu tại '{DATA_PATH}'. Vui lòng chạy data_collector.")
        return

    if len(df) < 20 or len(df['device_label'].unique()) < 2:
        print("Dữ liệu quá ít hoặc không đủ số lớp. Cần ít nhất 20 bản ghi và 2 nhãn khác nhau.")
        return
        
    # Chuyển đổi nhãn dạng chữ sang số
    le = LabelEncoder()
    df['label_encoded'] = le.fit_transform(df['device_label'])
    
    X = df.drop(['device_label', 'label_encoded'], axis=1)
    y = df['label_encoded']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    model = RandomForestClassifier(n_estimators=150, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nĐộ chính xác (Accuracy): {accuracy:.2f}")
    print("Báo cáo phân loại:")
    print(classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0))
    
    # Lưu cả model và bộ mã hóa nhãn
    model_bundle = {'model': model, 'label_encoder': le}
    joblib.dump(model_bundle, MODEL_PATH)
    print(f"✅ Mô hình và bộ mã hóa đã được lưu tại '{MODEL_PATH}'")

if __name__ == '__main__':
    train_identifier_model()