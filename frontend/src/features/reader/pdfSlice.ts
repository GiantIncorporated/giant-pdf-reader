import {createSlice, type PayloadAction} from "@reduxjs/toolkit";
import type {ReaderProps} from "../../types/reader.type.ts";


interface PdfState {
    pdfFile: ReaderProps
}

export const pdfSlice = createSlice({
    name: 'pdf',
    initialState: {
        pdfFile: {},
    } as PdfState,
    reducers: {

        savePdf: (state, action: PayloadAction<ReaderProps>) => {
            state.pdfFile = action.payload;
        },

        nextPage: (state) => {
            if (state.pdfFile.currentPage < state.pdfFile.page_count) {
                state.pdfFile.currentPage += 1;
            }
        },
        prevPage: (state) => {
            if (state.pdfFile.currentPage > 0) {
                console.log(`Prev page: ${state.pdfFile.currentPage - 1}`);
                state.pdfFile.currentPage -= 1;
            }
        }
    }
})

export const {savePdf, nextPage, prevPage} = pdfSlice.actions;
export default pdfSlice.reducer