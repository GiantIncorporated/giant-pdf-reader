import {createSlice} from "@reduxjs/toolkit";

export const pdfSlice = createSlice({
    name: 'pdf',
    initialState: {
        currentPage: 0,
    },
    reducers: {
        nextPage: state => {
            console.log(`Next page requested: ${state.currentPage + 1}`)
            state.currentPage += 1;
        },

        prevPage: state => {
            console.log(`Prev page requested: ${state.currentPage - 1}`)
            state.currentPage -= 1;
        }
    }
})

export const {nextPage, prevPage} = pdfSlice.actions;
export default pdfSlice.reducer