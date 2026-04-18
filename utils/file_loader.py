import os
import streamlit as st

def load_resource(file_path):
    """파일을 읽어서 텍스트를 반환 실패 시 빈 문자열을 반환하고 에러를 표시"""
    if not os.path.exists(file_path):
        st.error(f"파일을 찾을 수 없습니다: {file_path}")
        return ""
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"파일 로드 중 오류 발생 ({file_path}): {e}")
        return ""