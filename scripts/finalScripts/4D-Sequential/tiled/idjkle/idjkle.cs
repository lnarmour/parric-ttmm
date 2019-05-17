prog = ReadAlphabets("../../BlockTTMM.ab");
system = "BlockTTMM";
outDir = "out/";

CheckProgram(prog);
#Show(prog);
#AShow(prog);
#PrintAST(prog);

#set the spacetimeMap for the program
#Schedule 1
setSpaceTimeMap(prog, system, "C", "(i,j,k,l,d,e->i,d,j,k,l,e)",  "(i,j,k,l->i,0,j,k,l,0)");

#Schedule 1
#setSpaceTimeMap(prog, system, "C", "(i,j,k->j,i,k)");
#setSpaceTimeMap(prog, system, "C", "(i,j,k,l->i,j,k,l)");

#Schedule 2
#setSpaceTimeMap(prog, system, "C", "(i,j,k,l,d,e->i,j,d,k,l,e)");
#setMemorySpace(prog, system, "CSpace", "C, temp_C");
#setMemoryMap(prog, system, "temp_C", "CSpace", "(i,j,k->i,j)");
#setMemoryMap(prog, system, "C", "CSpace", "(i,j,k->i,j)");
#setStatementOrdering(prog, system, "temp_C", "C");
#setOrderingDimensions(prog, system, 0);
#setParallel(prog, system, "0", "1");
#setParallel(prog, system, "", "0,1");

#generateVerificationCode(prog, system, outDir);
#generateWriteC(prog, system, outDir);
generateWrapper(prog, system, outDir);
generateMakefile(prog, system, outDir);
generateScheduledCode(prog, system, outDir);