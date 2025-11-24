import { ViewMacsGrid } from '#components/grids';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('ViewMacsGrid', () => {
  let component: ViewMacsGrid;
  let fixture: ComponentFixture<ViewMacsGrid>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewMacsGrid],
    }).compileComponents();

    fixture = TestBed.createComponent(ViewMacsGrid);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
