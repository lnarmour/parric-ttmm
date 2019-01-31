void blockmult(const float* a, const float* b, float* c){
    for(int i=0;i<SIZE;i++)
        for(int k=0;k<SIZE;k++)
            for(int j=0;j<SIZE;j++)
                c[i*SIZE+j]+=a[i*SIZE+k]*b[k*SIZE+j];
}
